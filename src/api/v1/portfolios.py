import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from services.portfolio.portfolio_service import get_info

from api.v1.users import get_users_params

portfolio_bp = Blueprint("portfolios", __name__)


def get_params(current_user, portfolios=''):
    params = get_users_params(current_user)
    params['portfolios'] = portfolios
    return params


@portfolio_bp.route('/update', methods=['POST'])
@jwt_required()
def update_value():
    current_user = get_jwt_identity()
    portfolios = ''
    if request.method == 'POST' and request.form.get('strategy'):
        pass


@portfolio_bp.route('/', methods=['GET'])
@jwt_required()
def get_portfolios():
    current_user = get_jwt_identity()
    portfolios = get_info()
    return render_template('portfolio/portfolios_temp.html', **get_params(current_user, portfolios))
