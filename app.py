#from turtle import mode

from dash import ALL, Dash, State, ctx, html, dcc, Input, Output
from calculator import calculate_contributions
from components.expenses import expenses_layout
from components.people import people_layout
from components.results import results_layout
import os

port = int(os.environ.get("PORT", 8050))

def safe_float(val):
    try:
        return float(val)
    except:
        return 0

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([

    html.Div([
        html.H1("Joint Expense Calculator"),

        # --- Mode ---
        html.H3("Mode"),
        dcc.RadioItems(
            id="mode",
            options=[
                {"label": "Equal Split", "value": "equal"},
                {"label": "Proportional to Income", "value": "proportional"},
            ],
            value="equal"
        ),

        people_layout(),
        expenses_layout(),
        results_layout(),
    ], className="container")
])

@app.callback(
    Output("people-list", "children"),
    Input("people-data", "data")
)
def render_people(people):
    children = []
    for i, person in enumerate(people):
        children.append(
            html.Div([
                html.Label(f"Person {i+1}"),
                dcc.Input(
                    value=person["name"],
                    id={"type": "name", "index": i},
                    placeholder="Name",
                ),
                dcc.Input(
                    value=person["income"],
                    type="text",
                    id={"type": "income", "index": i},
                    placeholder="Income",
                ),
                html.Button(
                    "x",
                    id={"type": "remove-person", "index": i},
                    n_clicks=0,
                    className="remove-btn"
                )
             ], className="people-row"
            )
        )
    return children

@app.callback(
    Output("people-data", "data"),
    Input("add-person", "n_clicks"),
    Input({"type": "name", "index": ALL}, "value"),
    Input({"type": "income", "index": ALL}, "value"),
    Input({"type": "remove-person", "index": ALL}, "n_clicks"),
    State("people-data", "data")
)
def update_people(add_clicks, names, income, remove, people):
    if people is None:
        people = []
    triggered_id = ctx.triggered_id

    #If add person button triggered:
    if triggered_id == "add-person":
        people.append({
            "name": None,
            "income": None
        })
        return people
    
    #remove person
    if isinstance(triggered_id, dict) and triggered_id["type"] == "remove-person":
        index_to_remove = triggered_id["index"]
        return [p for i, p in enumerate(people) if i != index_to_remove]
    
    #If no dynamic inputs exists skip
    if not names or not income:
        return people
    
    #update people
    updated = []
    for i in range(len(names)):
        updated.append({
            "name": names[i],
            "income": income[i]
        })
    return updated


@app.callback(
    Output("results", "children"),
    Input("calculate_results", "n_clicks"),
    State("mode", "value"),
    State("rent", "value"),
    State("groceries", "value"),
    State("utilities", "value"),
    State("other", "value"),
    State("people-data", "data"),
)
def update_results(n_clicks, mode, rent, groceries, utilities, other, people):
    if n_clicks == 0:
        return ""

    if not people:
        return "Please add at least one person."

    expenses = {
        "rent": rent or 0,
        "groceries": groceries or 0,
        "utilities": utilities or 0,
        "other": other or 0,
    }

    total_expense = sum(expenses.values())
    people_float = [ {
        "name": p["name"],
        "income": safe_float(p["income"])
    } for p in people
    ]
    #call function to calculate contributions from calculator.py
    contributions = calculate_contributions(people_float, total_expense, mode)
    income_lookup = {
        p["name"]: safe_float(p["income"]) #if p["income"] not in [None, ""] #else 0
        for p in people
    }

    #make results visible:
    return html.Div([
        html.Span(
            "invalid input detected, treating as 0",
            className="warning"
        ) if any(
            p["income"] not in [None, ""] and safe_float(p["income"]) == 0
            for p in people
        ) else "",
        html.Div([
            html.Span(f"Total Expenses: ", className="result-total-label"),
            html.Span(f"€{total_expense:.2f}", className="result-total-value")
        ], className="result-total-row"),
        *[
        html.Div([
            html.Span(f"{name}:", className="result-name"),
            html.Span(f" €{amount:.2f}", className="result-amount"),

            html.Span(
                f" ({amount/total_expense*100:.1f}% of total expenses"
                + ( f"; {amount/income_lookup.get(name)*100:.1f}% of income)"),
                className="result-percentage"
            ) if total_expense > 0 and income_lookup.get(name) > 0 else "",
            #warning
            html.Span(
                "exceeds income!",
                className="warning"
            ) if amount > (income_lookup.get(name) or 0) else ""
        ], className="result-row")
        for name, amount in contributions.items()
        ]
    ])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    debug = os.environ.get("RENDER") is None  # debug only locally
    app.run(host="0.0.0.0", port=port, debug=debug)

#if __name__ == "__main__":
#    app.run(debug=True)