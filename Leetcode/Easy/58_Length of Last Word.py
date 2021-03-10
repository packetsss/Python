s = " "

ns = s[::-1]
if ns.find(" ") == -1:
    print(len(s))
elif list(s) == [" "]*len(s):
    print(0)
elif ns.find(" ") == 0:
    for i in range(0, len(ns)):
        if ns.find(" ", i) < ns.find(" ", i + 1) - 1:
            print((ns.find(" ", i + 1) - ns.find(" ", i) - 1))
            break
        elif ns.find(" ", i) < 0:
            print(s.find(" "))
else:
    print(ns.find(" "))

