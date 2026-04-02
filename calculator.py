def calculate_contributions(users, total_expense, mode):

    if len(users) == 0:
        return {}

    if mode == "equal":
        per_person = total_expense / len(users)
        return {u["name"]: per_person for u in users}

    elif mode == "proportional":
        total_income = sum(u["income"] for u in users)
        if total_income == 0:
            return {u["name"]: 0 for u in users}

        return {
            u["name"]: (u["income"] / total_income) * total_expense
            for u in users
        }