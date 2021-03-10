command = "G()(al)"

str1 = ""
for i in range(len(command)):
    if command[i] == "G":
        str1 += "G"
    elif command[i:i + 2] == "()":
        str1 += "o"
    elif command[i:i + 4] == "(al)":
        str1 += "al"

print(str1)
