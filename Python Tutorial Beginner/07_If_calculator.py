# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

num1 = float(input("Number 1:"))
num2 = float(input("Number 2:"))
op = str(input("Operation:"))

if op == "+":
    print(num1 + num2)
elif op == "-":
    print(num1 - num2)
elif op == "*":
    print(num1 * num2)
elif op == "/":
    print(num1 / num2)
else:
    print("Invalid Operation")
