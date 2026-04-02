from dash import html, dcc

def expenses_layout():
    return html.Div([
        html.H3("Expenses"),
        html.Div([
            html.Label("Rent"), 
            dcc.Input(id="rent", type="number", placeholder="€")
        ], className="expense-row"),
        html.Div([
            html.Label("Groceries"),
            dcc.Input(id="groceries", type="number", placeholder="€")
        ], className="expense-row"),
        html.Div([
            html.Label("Utilities"),
            dcc.Input(id="utilities", type="number", placeholder="€")
        ], className="expense-row"),
        html.Div([
            html.Label("Other Expenses"),
            dcc.Input(id="other", type="number", placeholder="€")
        ], className="expense-row"),
    ], className="card")