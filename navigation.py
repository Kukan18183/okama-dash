import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Database", href="/database")),
        dbc.NavItem(dbc.NavLink("Efficient Frontier", href="/")),
        dbc.NavItem(dbc.NavLink("Compare Assets", href="/compare")),
        dbc.NavItem(dbc.NavLink("Benchmark", href="/benchmark")),
        dbc.NavItem(dbc.NavLink("Portfolio", href="/portfolio")),
    ],
    brand="PFA",
    brand_href="/",
    color="#295249",
    dark=True,
    links_left=True,
)
