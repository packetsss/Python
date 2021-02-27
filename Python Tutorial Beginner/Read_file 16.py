file = open("Ex.txt", "r")

# print(file.readable())
# print(file.read())
print(file.readlines()[0])

# for employee in file.readlines():
#     print(employee)

file.close()

file = open("Ex2.txt", "w")

file.write("\nWhy am I sad?")

file.close()
