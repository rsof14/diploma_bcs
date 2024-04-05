import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from services.customer.customer_service import get_customers_list

from api.v1.users import get_users_params

customers_bp = Blueprint("customers", __name__)


def get_params(current_user, customers=''):
    params = get_users_params(current_user)
    params['customers'] = customers
    return params


@customers_bp.route('/', methods=['GET'])
@jwt_required()
def get_customers():
    current_user = get_jwt_identity()
    customers = get_customers_list()
    return render_template('customers/customers_temp.html', **get_params(current_user, customers))

