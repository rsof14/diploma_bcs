from dateutil.relativedelta import relativedelta
from db.queries.portfolio import get_all_portfolios_info, get_portfolio_by_id, update_risks
import datetime
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm


def get_info():
    return get_all_portfolios_info()


def update_portfolios_risks(portfolios_ids: dict):
    for portfolio in portfolios_ids['portfolios']:
        var = calculate_var(portfolio)
        update_risks('Value at Risk', portfolio, var)


def calculate_var(portfolio_id: str):
    portfolio = get_portfolio_by_id(portfolio_id)
    structure = portfolio.structure
    start_date = (datetime.datetime.now().date() - relativedelta(years=1)).strftime('%Y-%m-%d')
    end_date = (datetime.datetime.now().date() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    assets = list(structure.keys())
    nums = list(structure.values())
    prices = dict(zip(tuple(assets), yf.download(tuple(assets), start=end_date)['Close'].values[0] * nums))
    portfolio_value = sum(list(prices.values()))
    weights = {}
    for i in prices:
        weights[i] = float(prices[i] / portfolio_value)
    tickers_weights = pd.DataFrame(list(weights.items()), columns=['Ticker', 'Weight'])
    year_prices = pd.DataFrame(columns=assets)
    for ticker in assets:
        year_prices[ticker] = yf.download(ticker, start_date, end_date)['Close']
    returns = year_prices.pct_change()
    returns = returns[(returns.T != 0).any()]
    returns = returns.dropna()
    returns = returns.reset_index(drop=True)
    cov_matrix_df = returns.cov()
    cov_matrix = np.array(cov_matrix_df)
    tickers_weights['Weight'].values.transpose()
    stdev = np.sqrt(np.matmul(np.matmul(tickers_weights['Weight'].values, cov_matrix),
                              tickers_weights['Weight'].values.transpose()))
    var = round(stdev * np.sqrt(10) * norm.ppf(0.95) * 100, 3)

    return var
