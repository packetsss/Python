s = "RLLLLRRRLR"

ctl, ctr, ctt = 0, 0, 0
for i in s:
    if i == "L":
        ctl += 1
    elif i == "R":
        ctr += 1
    if ctl == ctr:
        ctt += 1
print(ctt)

