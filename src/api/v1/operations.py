import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from services.operation.operation_service import get_portfolio_list, form_portfolio_operations, send_portfolio_operations

from api.v1.users import get_users_params

operations_bp = Blueprint("operations", __name__)


def get_params(current_user, message='', operations='', portfolios_ids=''):
    portfolios_list = get_portfolio_list(current_user)
    params = get_users_params(current_user)
    params['message'] = message
    params['operations'] = operations
    params['portfolios'] = []
    params['portfolios_ids'] = portfolios_ids
    keys = ('id', 'account', 'strategy', 'customer', 'updated')
    for portfolio in portfolios_list:
        portfolio_params = dict(zip(keys, portfolio))
        params['portfolios'].append(portfolio_params)
    print(f"params {params}")
    return params


@operations_bp.route('/form', methods=['POST'])
@jwt_required()
def form_operations():
    current_user = get_jwt_identity()
    message = ''
    operations = ''
    portfolios_ids = {}
    if request.method == 'POST' and request.form.get('portfolios'):
        portfolios_ids = request.form.to_dict()
        portfolios_ids['portfolios'] = portfolios_ids['portfolios'].split(',')
        operations = form_portfolio_operations(portfolios_ids)
    portfolios = ''
    for p_id in portfolios_ids['portfolios']:
        portfolios += f"{p_id} "
    return render_template('operations/operations_temp.html', **get_params(current_user, message, operations, portfolios))


@operations_bp.route('/send', methods=['POST'])
@jwt_required()
def send_operations():
    print('send operations')
    print(f"portfolios {request.form.get('portfolios_')}")
    print(f"operations {request.form.get('total_operations')}")
    current_user = get_jwt_identity()
    message = ''
    if request.method == 'POST' and request.form.get('portfolios_') and request.form.get('total_operations'):
        portfolios_ids = request.form.get('portfolios_')
        # portfolios_ids['portfolios_'] = portfolios_ids['portfolios_'].split(',')
        send_portfolio_operations(request.form.get('portfolios_'), request.form.get('total_operations'))
        # message = f'Успешно сформированы операции и загружена заявка по портфелям: {" ".join(str(x) for x in portfolios_ids["portfolios_"])}'
        message = f'Успешно сформированы операции и загружена заявка по портфелям: {request.form.get("portfolios_")}'
    return render_template('operations/operations_temp.html', **get_params(current_user, message))


@operations_bp.route('/', methods=['GET'])
@jwt_required()
def get_operations():
    current_user = get_jwt_identity()
    return render_template('operations/operations_temp.html', **get_params(current_user))
