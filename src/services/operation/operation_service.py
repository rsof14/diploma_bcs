from db.queries.portfolio import get_portfolios_by_user, update_portfolio_status, get_portfolio_by_id, \
    get_strategy_info, get_latest_portfolio_value
from services.user.user_service import user_get_data
import logging
from sqlalchemy.exc import IntegrityError
import json
import yfinance as yf
import datetime
import math


def get_portfolio_list(login: str):
    user_id = user_get_data(login).id
    return get_portfolios_by_user(user_id)


def send_portfolio_operations(portfolios_ids: str, operations: str):
    print(f'new operations {operations}')
    print(portfolios_ids)
    portfolios = portfolios_ids[:-1].split(' ')
    print(portfolios)
    print(type(portfolios))
    try:
        for portfolio in portfolios:
            print(portfolio)
            update_portfolio_status(portfolio)
        logging.info('Portfolios %s successfully updated', portfolios_ids)
    except IntegrityError:
        logging.warning('Wrong')


def form_portfolio_operations(portfolios_ids: dict):
    quote_file = ''
    try:
        for portfolio in portfolios_ids['portfolios']:
            quote_file += form_quote(quote_file, portfolio)
            # update_portfolio_status(portfolio)
        logging.info('Portfolios %s successfully updated', portfolios_ids)
        print(quote_file)
    except IntegrityError:
        logging.warning('Wrong')

    return quote_file


def form_quote(document, portfolio_id):
    portfolio = get_portfolio_by_id(portfolio_id)
    structure = portfolio.structure
    strategy = get_strategy_info(portfolio.strategy_id)
    strategy_structure = strategy.structure
    tickers = list(strategy_structure.keys())
    start_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    costs = {}
    prices = dict(zip(tuple(tickers), yf.download(tuple(tickers), start=start_date)['Close'].values[0]))
    print(prices)
    total_cost = 0
    operations = ''
    for ticker in tickers:
        if ticker in list(structure.keys()):
            amount = structure[ticker]
        else:
            amount = 0
        costs[ticker] = amount * prices[ticker]
    portfolio_value = get_latest_portfolio_value(portfolio_id)
    if portfolio_value:
        total_cost = portfolio_value.value
    print(total_cost)

    if total_cost > 0:
        for ticker in tickers:
            current_weight = costs[ticker] / total_cost
            if ticker in list(strategy_structure.keys()):
                delta_weight = (strategy_structure[ticker] / 100) - current_weight
            else:
                delta_weight = -current_weight
            if delta_weight >= 0.01:
                price = prices[ticker]
                operation_amount = delta_weight * total_cost / price
                if operation_amount > 0:
                    operations += f'ACCOUNT={portfolio_id}; TICKER={ticker}; QUANTITY={math.floor(operation_amount)}; PRICE={round(price, 2)}; OPERATION=BUY;\n'
                elif operation_amount < 0:
                    operations += f'ACCOUNT={portfolio_id}; TICKER={ticker}; QUANTITY={math.ceil(operation_amount)}; PRICE={round(price, 2)}; OPERATION=SELL;\n'

    return operations
