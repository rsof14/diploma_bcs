from db.queries.portfolio import get_portfolios_by_user, update_portfolio_status_structure, get_portfolio_by_id, \
    get_strategy_info, get_latest_portfolio_value, update_portfolio_value, get_portfolios_values
from services.user.user_service import user_get_data
import logging
from sqlalchemy.exc import IntegrityError
import yfinance as yf
import datetime
import math
import random


def get_portfolio_list(login: str):
    user_id = user_get_data(login).id
    return get_portfolios_by_user(user_id)


def parse_operations(operations: str):
    final = {}
    for operation in operations.split('\n'):
        operation_ = operation.replace(" ", "").split(';')
        account, ticker, quantity, op = '', '', 0, ''
        for atr in operation_:
            atr_ = atr.split('=')
            if atr_[0] == 'ACCOUNT':
                account = atr_[1]
            elif atr_[0] == 'TICKER':
                ticker = atr_[1]
            elif atr_[0] == 'QUANTITY':
                quantity = atr_[1]
            elif atr_[0] == 'OPERATION':
                op = atr_[1]
        if account != '':
            quantity = int(quantity)
            if op == 'SELL':
                quantity *= -1
            if account not in final:
                final[account] = {}
            final[account][ticker] = quantity
    return final


def update_portfolio_structure(portfolio_id: str, operations: dict):
    portfolio = get_portfolio_by_id(portfolio_id)
    structure = portfolio.structure
    for ticker, value in operations.items():
        if ticker in structure:
            structure[ticker] += value
        else:
            structure[ticker] = value

    return structure


def send_portfolio_operations(portfolios_ids: str, operations: str):
    portfolios = portfolios_ids[:-1].split(' ')
    with open("/var/lib/auth/data/operations.txt", "w") as file:
        file.write(operations)
    parsed_operations = parse_operations(operations)
    try:
        for portfolio in portfolios:
            structure = update_portfolio_structure(portfolio, parsed_operations[portfolio])
            update_portfolio_status_structure(portfolio, structure)
        logging.info('Portfolios %s successfully updated', portfolios_ids)
    except IntegrityError:
        logging.warning('Wrong')


def form_portfolio_operations(portfolios_ids: dict):
    quote_file = ''
    try:
        for portfolio in portfolios_ids['portfolios']:
            quote_file += form_quote(portfolio)
        logging.info('Portfolios %s successfully updated', portfolios_ids)
    except IntegrityError:
        logging.warning('Wrong')

    return quote_file


def form_quote(portfolio_id):
    portfolio = get_portfolio_by_id(portfolio_id)
    structure = portfolio.structure
    strategy = get_strategy_info(portfolio.strategy_id)
    strategy_structure = strategy.structure
    tickers = list(strategy_structure.keys())
    start_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
    costs = {}
    try:
        prices = dict(zip(tuple(tickers), yf.download(tuple(tickers), start=start_date)['Close'].values[0]))
    except IndexError:
        days = 0
        df = yf.download(tuple(tickers), start=start_date)['Close']
        while df.shape[0] == 0:
            days += 1
            start_date = (datetime.datetime.now().date() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
            df = yf.download(tuple(tickers), start=start_date)['Close']
        prices = dict(zip(tuple(tickers), df.values[0]))
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


def get_value(portfolio_id: str, cur_value: float):
    return cur_value * random.choice([random.uniform(0.7, 1), random.uniform(1.1, 1.4)])


def update_portfolios():
    values = {}
    for portfolio in get_portfolios_values():
        values[portfolio.account] = get_value(portfolio.account, portfolio.value)
    update_portfolio_value(values)

    print('updated')
