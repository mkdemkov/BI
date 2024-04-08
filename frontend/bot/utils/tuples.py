def show_tuples(tuples: []) -> str:
    res = ""
    print(type(tuples))
    if len(tuples) == 1:
        for tup in tuples:
            res += f"<b>{tup[0]}</b> "
            tup = tup[1:]
            tup_str = [str(item) for item in tup]
            res += ";".join(tup_str)
            res += "\n"

    else:
        first_five = tuples[0]
        last_five = tuples[1]
        for tup in first_five:
            res += f"<b>{tup[0]}</b> "
            tup = tup[1:]
            tup_str = [str(item) for item in tup]
            res += ";".join(tup_str)
            res += "\n"
        res += ".........\n\n"
        for tup in last_five:
            res += f"<b>{tup[0]}</b> "
            tup = tup[1:]
            tup_str = [str(item) for item in tup]
            res += ";".join(tup_str)
            res += "\n"
    return res