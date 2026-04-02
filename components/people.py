from dash import html, dcc

def people_layout():
    return html.Div([
        html.H3("People"),
        html.Button("Add Person", id="add-person", n_clicks=0, className="button"),
        dcc.Store(id="people-data", data=[]),
        html.Div(id="people-list"),
    ], className="card")