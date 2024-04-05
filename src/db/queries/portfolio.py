from uuid import UUID

from db.models import User, Portfolio, Strategy, Customer, PortfolioValue, RiskProfile, PortfolioRisks
from db.pg_db import db
from sqlalchemy import desc
import datetime


def get_portfolios_by_user(user_id: UUID):
    return Portfolio.query.outerjoin(Strategy, Strategy.id == Portfolio.strategy_id).join(Customer,
                                                                                          Customer.id == Portfolio.customer_id).add_columns(
        Portfolio.account, Strategy.name, Customer.name, Portfolio.updated).filter(
        Portfolio.asset_manager == user_id).all()


def get_portfolio_by_id(portfolio_id: str):
    return Portfolio.query.filter_by(account=portfolio_id).first()


def update_portfolio_status_structure(portfolio_id: str, structure: dict):
    portfolio_obj = Portfolio.query.filter_by(account=portfolio_id).first()
    portfolio_obj.updated = True
    portfolio_obj.structure = structure
    db.session.commit()


def get_strategy_info(strategy_id: UUID):
    return Strategy.query.filter_by(id=strategy_id).first()


def get_latest_portfolio_value(account: str):
    return PortfolioValue.query.filter_by(account=account).order_by(desc(PortfolioValue.date)).first()


def update_portfolio_value(portfolio_values: dict):
    portfolios = Portfolio.query.all()
    portfolios_risks = PortfolioRisks.query.all()
    date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    for portfolio in portfolios:
        item = PortfolioValue(account=portfolio.account, date=date, value=portfolio_values[portfolio.account])
        portfolio.updated = False
        db.session.add(item)

    for pr in portfolios_risks:
        pr.updated = False

    db.session.commit()


def get_portfolios_values():
    return PortfolioValue.query.all()


def get_all_portfolios_info():
    last_date = PortfolioValue.query.order_by(desc(PortfolioValue.date)).first().date
    subq = PortfolioValue.query.filter_by(date=last_date).subquery()
    pcs = Portfolio.query.outerjoin(Strategy, Strategy.id == Portfolio.strategy_id).join(
        Customer, Customer.id == Portfolio.customer_id).outerjoin(subq, Portfolio.account == subq.c.account).outerjoin(RiskProfile,
        Strategy.risk_profile == RiskProfile.name).outerjoin(PortfolioRisks, Portfolio.account == PortfolioRisks.account).add_columns(
        Portfolio.account.label('account'), Customer.name.label('customer_name'), Strategy.name.label('strategy_name'), subq.c.value.label('value'), RiskProfile.max_var.label('max_var'), PortfolioRisks.risk_metric.label('risk_metric'), PortfolioRisks.value.label('metric_value'), PortfolioRisks.violation.label('violation'), PortfolioRisks.updated.label('updated'))
    return pcs.all()


def update_risks(metric: str, account: str, value: float):
    portfolio_risks = PortfolioRisks.query.filter_by(account=account, risk_metric=metric).first()
    max_var = Portfolio.query.filter_by(account=account).join(Strategy, Strategy.id == Portfolio.strategy_id).outerjoin(RiskProfile, Strategy.risk_profile == RiskProfile.name).add_columns(RiskProfile.max_var.label('max_var')).first().max_var
    if portfolio_risks:
        portfolio_risks.value = value
        portfolio_risks.updated = True
        portfolio_risks.violation = True if value > max_var else False
    else:
        item = PortfolioRisks(risk_metric=metric, account=account, value=value, updated=True, violation=True if value > max_var else False)
        db.session.add(item)

    db.session.commit()



