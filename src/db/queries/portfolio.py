from uuid import UUID

from db.models import User, Portfolio, Strategy, Customer, PortfolioValue
from db.pg_db import db
from sqlalchemy import desc


def get_portfolios_by_user(user_id: UUID):
    return Portfolio.query.outerjoin(Strategy, Strategy.id == Portfolio.strategy_id).join(Customer,
                                                                                          Customer.id == Portfolio.customer_id).add_columns(
        Portfolio.account, Strategy.name, Customer.name, Portfolio.updated).filter(
        Portfolio.asset_manager == user_id).all()


def get_portfolio_by_id(portfolio_id: str):
    return Portfolio.query.filter_by(account=portfolio_id).first()


def update_portfolio_status(portfolio_id: str):
    portfolio_obj = Portfolio.query.filter_by(account=portfolio_id).first()
    portfolio_obj.updated = True
    db.session.commit()


def get_strategy_info(strategy_id: UUID):
    return Strategy.query.filter_by(id=strategy_id).first()


def get_latest_portfolio_value(account: str):
    return PortfolioValue.query.filter_by(account=account).order_by(desc(PortfolioValue.date)).first()


def update_portfolio_value(portfolio_values: dict):
    value_objects = PortfolioValue.query.all()
    portfolio_objects = Portfolio.query.all()
    num = Portfolio.query.count()
    for i in range(num):
        obj = value_objects[i]
    # for obj in value_objects:
        if obj.account in list(portfolio_values.keys()):
            obj.value = portfolio_values[obj.account]
        portfolio_objects[i].updated = False

    # for portfolio in portfolio_objects:
    #     portfolio.updated = False
    db.session.commit()


def get_portfolios_values():
    return PortfolioValue.query.all()
