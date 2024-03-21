def show_tuples(tuples: []) -> str:
    res = ""
    print(type(tuples))
    if len(tuples) <= 10:
        print(tuples)
        print("-----")
        for tup in tuples:
            res += f"<b>{tup[0]}</b> "
            tup = tup[1:]
            tup_str = [str(item) for item in tup]
            res += ";".join(tup_str)
            res += "\n"

    else:
        first_five = tuples[:5]
        last_five = tuples[len(tuples) - 5:]
        for tup in first_five:
            res += f"<b>{tup[0]}</b> "
            tup = tup[1:]
            tup_str = [str(item) for item in tup]
            res += ";".join(tup_str)
            res += "\n"
        res += "..."
        for tup in last_five:
            res += f"<b>{tup[0]}</b> "
            tup = tup[1:]
            tup_str = [str(item) for item in tup]
            res += ";".join(tup_str)
            res += "\n"
    return res


def create_tuples(csv_file) -> []:
    pass