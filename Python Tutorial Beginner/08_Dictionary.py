month_conv = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
}

print(month_conv.get("Jan", "Not a valid key"))

calc_conv = {
    1: "+",
    2: "-",
    3: "*",
    4: "/",
}

print(calc_conv.get(3))
