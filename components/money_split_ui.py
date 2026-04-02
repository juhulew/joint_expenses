#money split
#use dash:



#logic:

#people
#expenses
#mode toggle
#optional:
# income stress indicator
# warn if so pays > 40% of their income
# Savings-aware mode
# users define how much money they want to save themselves
# Rounding logic
# Round to nearest €10 for real-world usability
# Presets
# Save household setups

total_expenses = sum(expenses.values())

if mode == "equal":
    per_person = total_expenses / len(users)

elif mode == "proportional":
    total_income = sum(u["income"] for u in users)
    contributions = {
        u["name"]: (u["income"] / total_income) * total_expenses
        for u in users
    }




#data model example:

users = [
    {"name": "Jule", "income": 500},
    {"name": "Nils", "income": 2000},
]

expenses = {
    "rent": 850,
    "groceries": 400, #tbt
    "utilities": 200, #split to wifi, electricity, gez
}