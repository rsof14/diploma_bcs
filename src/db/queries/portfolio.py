from uuid import UUID

from db.models import User, Portfolio, Strategy, Customer
from db.pg_db import db


def get_portfolios_by_user(user_id: UUID):
    return Portfolio.query.outerjoin(Strategy, Strategy.id == Portfolio.strategy_id).join(Customer, Customer.id == Portfolio.customer_id).add_columns(
        Portfolio.account, Strategy.name, Customer.name, Portfolio.updated).filter(Portfolio.asset_manager == user_id).all()

