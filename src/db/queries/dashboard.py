from uuid import UUID

from db.models import Strategy, Customer, PortfolioValue
from db.pg_db import db
from sqlalchemy import desc


def get_strategies_for_dashboard():
    return Strategy.query.filter_by(type='Регламентная', valid=True).all()


def get_strategy_by_name(name: str):
    return Strategy.query.filter_by(name=name).first()
