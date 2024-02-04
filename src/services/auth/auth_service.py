import logging

import json
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token

from core.config import app_config
from db.queries.user import get_user_by_login, add_login_history_record
from db.pg_db import db
from services.auth.passwords import hash_password, verify_password
from services.auth.jwt_init import jwt
from db.redis_storage import jwt_redis_blocklist


class UserIncorrectLoginData(Exception):
    ...


class UserIncorrectPassword(Exception):
    ...


# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@jwt.additional_claims_loader
def user_claims_to_access_token(user_login):
    user = get_user_by_login(user_login)
    user_role = user.role_id
    user_claim = {
        'id': str(user.id),
        'name': user.name,
        'is_superuser': user.is_superuser,
        'roles': str(user_role),
    }
    return {'user_info': json.dumps(user_claim)}


def add_token_to_block_list(jti, token_type):
    ttl = app_config.JWT_ACCESS_TOKEN_EXPIRES if token_type == 'access' else app_config.JWT_REFRESH_TOKEN_EXPIRES
    jwt_redis_blocklist.set(jti, "", ex=ttl)


def generate_token_pair(identity):
    tokens = {
        'access_token': create_access_token(identity=identity),
        'refresh_token': create_refresh_token(identity=identity)
    }
    return tokens


def login_user(login: str, password: str, user_agent: str):
    user = get_user_by_login(login)
    if not user or not verify_password(password=password, hashed_password=user.password):
        raise UserIncorrectLoginData('Login or password is incorrect')

    tokens = generate_token_pair(identity=user.login)
    add_login_history_record(user_id=user.id, user_agent=user_agent)
    return tokens


def change_user_pw(login: str, password: str, new_password: str):
    user = get_user_by_login(login)
    if verify_password(password=password, hashed_password=user.password):
        user.password = hash_password(new_password)
        db.session.commit()
        logging.info('User password in db %s updated successfully', login)
    else:
        logging.warning('User password in db %s is incorrect', login)
        raise UserIncorrectPassword('Incorrect old password')
