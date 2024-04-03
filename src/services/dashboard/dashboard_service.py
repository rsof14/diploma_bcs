from db.queries.dashboard import get_strategies_for_dashboard, get_strategy_by_name
import plotly
import plotly.express as px
import pandas as pd
import json
import yfinance as yf
import datetime


def get_strategies():
    strategies = get_strategies_for_dashboard()
    return strategies


def form_diagrams(strategy_name: str):
    strategy = get_strategy_by_name(strategy_name)
    data = strategy.structure
    assets = list(data.keys())
    values = list(data.values())
    start_date = (datetime.datetime.now().date() - datetime.timedelta(days=31)).strftime('%Y-%m-%d')
    end_date = (datetime.datetime.now().date() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    return [form_strategy_structure_diagram(assets, values), form_strategy_sectors_diagram(assets, values),
            form_strategy_profit_dynamic(strategy_name, assets, start_date, end_date),
            form_strategy_prices_dynamic(assets, start_date, end_date)]


def form_strategy_structure_diagram(assets: list, values: list):
    df = pd.DataFrame({'ticker': assets, 'proportion': values})
    fig = px.pie(df,
                 values='proportion',
                 names='ticker',
                 color_discrete_sequence=px.colors.sequential.Plasma,
                 )
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',

    )
    fig.update_layout(uniformtext_minsize=10,
                      title_text='Состав стратегии',
                      title_x=0.5,
                      font=dict(
                          family='Montserrat, monospace',
                          size=18,
                          color="black"
                      ),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      width=400,
                      height=320,
                      )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def form_strategy_sectors_diagram(assets: list, values: list):
    sectors = []
    for asset in assets:
        company = yf.Ticker(asset)
        try:
            sectors.append(company.info['sector'])
        except KeyError:
            sectors.append('Undefined')
    df_sector = pd.DataFrame({'sector': sectors, 'proportion': values})
    fig = px.pie(df_sector,
                 values='proportion',
                 names='sector',
                 color_discrete_sequence=px.colors.sequential.BuPu_r,
                 )
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',

    )
    fig.update_layout(uniformtext_minsize=10,
                      title_text='Состав по секторам',
                      title_x=0.5,
                      font=dict(
                          family='Montserrat, monospace',
                          size=18,
                          color="black"
                      ),
                      showlegend=False,
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      width=400,
                      height=320,
                      )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def form_strategy_prices_dynamic(assets: list, start_date: str, end_date: str):
    data = pd.DataFrame(columns=assets)
    for asset in assets:
        data[asset] = yf.download(asset, start_date, end_date)['Close']
    changes = (data.values[-1] - data.values[0]) / data.values[0] * 100
    df_changes = pd.DataFrame({'ticker': assets, 'variation': changes})
    fig = px.bar(df_changes, x='ticker', y='variation', color_discrete_sequence=px.colors.sequential.Purp_r)
    fig.update_layout(uniformtext_minsize=10,
                      title=dict(text='Изменение цен за месяц', x=0.5, font=dict(
                          family='Montserrat, monospace',
                          size=18,
                          color="black"
                      )),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      width=600,
                      height=290,
                      )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def form_strategy_profit_dynamic(strategy_name: str, assets: list, start_date: str, end_date: str):
    assets_benchmark = assets
    assets_benchmark.append('^GSPC')
    df = pd.DataFrame(columns=assets_benchmark)
    for ticker in assets_benchmark:
        df[ticker] = yf.download(ticker, start_date, end_date)['Close']
    res = pd.DataFrame(columns=['Strategy sum', 'S&P 500 sum'])
    sum = 0
    for ticker in assets:
        sum += df[ticker]
    res['Strategy sum'] = sum
    res['S&P 500 sum'] = df['^GSPC']
    res[strategy_name] = res['Strategy sum'] / res.iloc[0]['Strategy sum'] * 100
    res['S&P 500'] = res['S&P 500 sum'] / res.iloc[0]['S&P 500 sum'] * 100
    fig = px.line(res[[strategy_name, 'S&P 500']],
                  title="Доходность стратегии (в сравнении с бенчмарком)", markers=True,
                  color_discrete_map={strategy_name: '#4100bb', 'S&P 500': '#aea8b8'})
    fig.update_layout(uniformtext_minsize=10,
                      title=dict(x=0.5, font=dict(
                          family='Montserrat, monospace',
                          size=18,
                          color="black"
                      )),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      width=600,
                      height=290
                      )
    fig.update_traces(
        selector={"name": "S&P 500"},
        line={"dash": "dash"}
    )
    fig.update_layout(xaxis_title='', yaxis_title='')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
