import re

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State

from dash.exceptions import PreventUpdate

import pandas as pd

from common import settings as settings, inflation as inflation
from common.symbols import get_symbols
from common import cache

app = dash.get_app()
cache.init_app(app.server)

options = get_symbols()

today_str = pd.Timestamp.today().strftime("%Y-%m")
card_controls = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Efficient Frontier", className="card-title"),
            html.Div(
                [
                    html.Label("Tickers in the Efficient Frontier"),
                    dcc.Dropdown(
                        options=options,
                        value=settings.default_symbols,
                        multi=True,
                        placeholder="Select assets",
                        id="ef-symbols-list",
                    ),
                ],
            ),
            html.Div(
                [
                    html.Label("Base currency"),
                    dcc.Dropdown(
                        options=inflation.get_currency_list(),
                        value="USD",
                        multi=False,
                        placeholder="Select a base currency",
                        id="ef-base-currency",
                    ),
                ],
            ),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("First Date"),
                                    dbc.Input(
                                        id="ef-first-date", value="2000-01", type="text"
                                    ),
                                    dbc.FormText("Format: YYYY-MM"),
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.Label("Last Date"),
                                    dbc.Input(
                                        id="ef-last-date", value=today_str, type="text"
                                    ),
                                    dbc.FormText("Format: YYYY-MM"),
                                ]
                            ),
                        ]
                    )
                ]
            ),
            html.Div(
                [
                    dbc.Button(
                        children="Get the Efficient Frontier",
                        id="ef-submit-button-state",
                        n_clicks=0,
                        color="primary",
                    ),
                ],
                style={"text-align": "center"},
                className="p-3",
            ),
        ]
    ),
    class_name="mb-3",
)

#
# @app.callback(
#     Output("ef-symbols-list", "options"),
#     Input("ef-symbols-list", "search_value"),
#     State("ef-symbols-list", "value"),
# )
# def update_options(search_value, value):
#     if not search_value:
#         raise PreventUpdate
#     opt_list = [
#         o for o in options if re.match(search_value, o, re.IGNORECASE) or o in (value or [])
#     ]
#     return opt_list
