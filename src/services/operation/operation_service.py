from db.queries.portfolio import get_portfolios_by_user, update_portfolio_status, get_portfolio_by_id, get_strategy_info
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


def form_portfolio_operations(portfolios_ids: dict):
    quote_file = ''
    try:
        for portfolio in portfolios_ids['portfolios']:
            quote_file += form_quote(quote_file, portfolio)
            update_portfolio_status(portfolio)
        logging.info('Portfolios %s successfully updated', portfolios_ids)
        print(quote_file)
    except IntegrityError:
        logging.warning('Wrong')


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
        print(list(structure.keys()))
        if ticker in list(structure.keys()):
            amount = structure[ticker]
        else:
            amount = 0
        # price = float(yf.download(ticker, start=start_date)['Close'].iloc[0])
        # prices[ticker] = price
        # costs[ticker] = amount * price
        costs[ticker] = amount * prices[ticker]
        total_cost += costs[ticker]
        if total_cost == 0:
            total_cost = 1000

    for ticker in tickers:
        current_weight = costs[ticker] / total_cost
        # if total_cost != 0:
        #     current_weight = costs[ticker] / total_cost
        # else:
        #     current_weight = 0
        if ticker in list(strategy_structure.keys()):
            delta_weight = (strategy_structure[ticker] / 100) - current_weight
        else:
            delta_weight = -current_weight
        print(f'delta weight {delta_weight}')
        if delta_weight >= 0.01:
            price = prices[ticker]
            operation_amount = delta_weight * total_cost / price
            print(f'operation amount {operation_amount}')
            if operation_amount > 0:
                operations += f'{portfolio_id} {ticker} {math.ceil(operation_amount)} {price} buy\n'
            elif operation_amount < 0:
                operations += f'{portfolio_id} {ticker} {math.ceil(-operation_amount)} {price} sell\n'

    return operations





