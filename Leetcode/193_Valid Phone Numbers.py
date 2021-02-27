
with open("file.txt", "r") as f:
    counter = 0
    string = ""
    for i in f:
        if "-" in i[3] and i[7]:
            string += i
        if "(" in i[0] and ")" in i[4] and "-" in i[9]:
            string += i

print(string)

# only taking Bash??