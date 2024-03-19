import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from services.dashboard.dashboard_service import get_strategies, form_diagram

from api.v1.users import get_users_params

dashboard_bp = Blueprint("dashboard", __name__)


def get_params(current_user, strategies, selected_strategy='', diagram=''):
    params = get_users_params(current_user)
    params['strategies'] = strategies
    params['selected'] = selected_strategy
    params['diagram'] = diagram
    return params


@dashboard_bp.route('/form', methods=['POST'])
@jwt_required()
def form_dashboard():
    current_user = get_jwt_identity()
    strategy = ''
    diagram = ''
    if request.method == 'POST' and request.form.get('strategy'):
        strategy = request.form.get('strategy')
        diagram = form_diagram(strategy)
    strategies = get_strategies()
    return render_template('dashboard/dashboard_temp.html', **get_params(current_user, strategies, strategy, diagram))


@dashboard_bp.route('/', methods=['GET'])
@jwt_required()
def get_dashboard():
    current_user = get_jwt_identity()
    strategies = get_strategies()
    return render_template('dashboard/dashboard_temp.html', **get_params(current_user, strategies))
