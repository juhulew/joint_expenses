from dash import html, dcc

def results_layout():
    return html.Div([
        html.H3("Result"),
        html.Button(
            "Calculate", 
            id="calculate_results", 
            n_clicks=0,
            style={
                "padding": "10px 20px",
                "backgroundColor": "#187272",
                "color": "white",
                "border": "none",
                "borderRadius": "5px",
                "cursor": "pointer",
                "marginTop": "10px", 
                "marginBottom": "15px"
            }
        ),
        html.Div(id="results"),
    ], className="card")