import dash
import dash_bootstrap_components as dbc
import okama
import okama as ok
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State

from common.mobile_screens import adopt_small_screens
from common.parse_query import make_list_from_string
from pages.efficient_frontier.cards_efficient_frontier.ef_chart import \
    card_graf
from pages.efficient_frontier.cards_efficient_frontier.ef_chart_transition_map import \
    card_transition_map
from pages.efficient_frontier.cards_efficient_frontier.ef_controls import \
    card_controls
from pages.efficient_frontier.cards_efficient_frontier.ef_info import \
    card_ef_info
from pages.efficient_frontier.prepare_ef_plot import (prepare_ef,
                                                      prepare_transition_map)

dash.register_page(
    __name__,
    path="/",
    title="PFA: Efficient Frontier",
    name="Efficient Frontier",
)


def layout(tickers=None, first_date=None, last_date=None, ccy=None, **kwargs):
    tickers_list = make_list_from_string(tickers)
    page = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(card_controls(tickers_list, first_date, last_date, ccy), lg=7),
                    dbc.Col(card_ef_info, lg=5),
                ]
            ),
            dbc.Row(dbc.Col(card_graf, width=12), align="center"),
            dbc.Row(
                html.Div(
                    [
                        dcc.Markdown(
                            """
                        **Portfolio data**  
                        Click on points to get portfolio data.
                        """
                        ),
                        html.P(id="ef-click-data-risk"),
                        html.P(id="ef-click-data-return"),
                        html.Pre(id="ef-click-data-weights"),
                    ]
                ),
            ),
            dbc.Row(dbc.Col(card_transition_map, width=12), align="center"),
        ],
        class_name="mt-2",
        fluid="md",
    )
    return page


@callback(
    Output(component_id="ef-graf", component_property="figure"),
    Output(component_id="ef-transition-map-graf", component_property="figure"),
    Output(component_id="ef-graf", component_property="config"),
    Output(component_id="ef-transition-map-graf", component_property="config"),
    Output(component_id="ef-transition-map-graf-div", component_property="hidden"),  # hide TM chart
    # Inputs
    Input(component_id="store", component_property="data"),
    # Main input for EF
    Input(component_id="ef-submit-button-state", component_property="n_clicks"),
    State(component_id="ef-symbols-list", component_property="value"),
    State(component_id="ef-base-currency", component_property="value"),
    State(component_id="ef-first-date", component_property="value"),
    State(component_id="ef-last-date", component_property="value"),
    # Options
    State(component_id="ef-plot-options", component_property="value"),
    State(component_id="cml-option", component_property="value"),
    State(component_id="risk-free-rate-option", component_property="value"),
    # Monte-Carlo
    State(component_id="monte-carlo-option", component_property="value"),
    # Transition Map
    State(component_id="transition-map-option", component_property="value"),
    # Input(component_id="ef-return-type-checklist-input", component_property="value"),
    prevent_initial_call=False,
)
def update_ef_cards(
    screen,
    n_clicks,
    # Main input
    selected_symbols: list,
    ccy: str,
    fd_value: str,
    ld_value: str,
    # Options
    plot_option: str,
    cml_option: str,
    rf_rate: float,
    n_monte_carlo: int,
    tr_map_option: str,
):
    symbols = selected_symbols if isinstance(selected_symbols, list) else [selected_symbols]
    ef_object = ok.EfficientFrontier(
        symbols,
        first_date=fd_value,
        last_date=ld_value,
        ccy=ccy,
        inflation=False,
        n_points=40,
        full_frontier=True,
    )
    ef_options = dict(plot_type=plot_option, cml=cml_option, rf_rate=rf_rate, n_monte_carlo=n_monte_carlo)
    ef = ef_object.ef_points * 100
    fig1 = prepare_ef(ef, ef_object, ef_options)
    fig2 = prepare_transition_map(ef)

    # Change layout for mobile screens
    fig1, config1 = adopt_small_screens(fig1, screen)
    fig2, config2 = adopt_small_screens(fig2, screen)

    # Hide Transition map
    transition_map_is_hidden = False if tr_map_option == "On" else True
    return fig1, fig2, config1, config2, transition_map_is_hidden


@callback(
    Output("ef-click-data-risk", "children"),
    Output("ef-click-data-return", "children"),
    Output("ef-click-data-weights", "children"),
    Input("ef-graf", "clickData"),
    # List of tickers
    Input(component_id="ef-submit-button-state", component_property="n_clicks"),
    State(component_id="ef-symbols-list", component_property="value"),
)
def display_click_data(clickData, n_clock, symbols):
    """
    Display portfolio weights, risk and return.
    """
    if not clickData:
        raise dash.exceptions.PreventUpdate
    risk = clickData["points"][0]["x"]
    rist_str = f"Risk: {risk:.2f}%"

    ror = clickData["points"][0]["y"]
    ror_str = f"Return: {ror:.2f}%"

    weights_str = None
    try:
        weights_list = clickData["points"][0]["customdata"]
    except KeyError:
        pass
    else:
        weights_str = "Weights:" + ",".join([f" {t}={w:.2f}% " for w, t in zip(weights_list, symbols)])
    return rist_str, ror_str, weights_str
