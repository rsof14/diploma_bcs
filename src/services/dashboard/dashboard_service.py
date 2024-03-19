from db.queries.dashboard import get_strategies_for_dashboard, get_strategy_by_name
from matplotlib import pyplot as plt
import numpy as np
import plotly.graph_objs as go
import plotly
import dash_core_components as dcc
import dash_html_components as html
import json


def get_strategies():
    strategies = get_strategies_for_dashboard()
    return strategies


def form_diagram(strategy_name: str):
    strategy = get_strategy_by_name(strategy_name)
    data = strategy.structure
    assets = list(data.keys())
    values = list(data.values())
    print(f'{assets} {values}')
    trace = go.Pie(labels=assets, values=values)
    data = [trace]
    fig = go.Figure(data=data)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

