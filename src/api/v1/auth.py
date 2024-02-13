import logging
from http import HTTPStatus

from flask import jsonify, request, Blueprint, render_template
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from marshmallow import ValidationError
from api.v1.models.auth import login_in, login_out
from services.auth.auth_service import (
    login_user,
    UserIncorrectLoginData,
    add_token_to_block_list,
    generate_token_pair
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    user_agent = request.headers.get('User-Agent', default='unknown device')
    try:
        user = login_in.load(json_data)
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        tokens = login_user(user['login'], user['password'], user_agent=user_agent)
        logging.info('User with email %s successfully logged in', user['login'])
    except UserIncorrectLoginData as err:
        logging.warning('User with email %s denied to login: incorrect login or password', user['login'])
        return jsonify(message=str(err)), HTTPStatus.UNAUTHORIZED

    return login_out.dump(tokens)


@auth_bp.route('/check_access_token', methods=['POST'])
@jwt_required()
def check_access_token():
    current_user = get_jwt().get('user_info')
    return jsonify(current_user), HTTPStatus.OK


@auth_bp.route('/logout', methods=['POST'])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    token_type = token['type']
    logging.info('Token_type: %s', token_type)
    add_token_to_block_list(token['jti'], token_type)

    return jsonify(msg=f'{token_type} token successfully revoked')


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    tokens = generate_token_pair(identity)

    return login_out.dump(tokens)


@auth_bp.route('/', methods=['GET'])
def home():
    return render_template('auth/login/index.html')
