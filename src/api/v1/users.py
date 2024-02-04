import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from api.v1.models.common import paginate_in
from api.v1.models.users import change_password, login_history_paginated, user_schema
from services.auth.auth_service import UserIncorrectPassword, change_user_pw
from services.user.user_service import (
    LoginAlreadyExists,
    user_get_data,
    user_login_history
)

users_bp = Blueprint("user", __name__)


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    user_data = user_get_data(current_user)
    result = user_schema.dump(user_data)

    return jsonify(result), HTTPStatus.OK


@users_bp.route('/profile/login_history', methods=['GET'])
@jwt_required()
def get_login_history():
    current_user = get_jwt_identity()
    pagination = paginate_in.load(request.args)
    login_history_data = user_login_history(current_user, pagination.get('page'), pagination.get('page_size'))
    result = login_history_paginated.dump(login_history_data)
    return jsonify(result), HTTPStatus.OK


@users_bp.route('/profile/change_password', methods=['PUT'])
@jwt_required()
def change_user_password():
    current_user = get_jwt_identity()
    user_password_data = request.get_json()
    try:
        body = change_password.load(user_password_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    try:
        change_user_pw(current_user, body['old_password'], body['new_password'])
        logging.info('User with email %s updated password successfully', current_user)
    except UserIncorrectPassword as err:
        logging.warning('User with email %s denied to change password: incorrect old password', current_user)
        return jsonify(message=str(err)), HTTPStatus.CONFLICT

    return {'message': 'User password updated successfully'}, HTTPStatus.CREATED