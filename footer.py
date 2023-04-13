import dash
from dash import html, dcc


def footer():
    return html.Footer(
        html.Div(
            [
                html.Hr(),
            ],
            style={"text-align": "center"},
            className="p-3",
        ),
    )
