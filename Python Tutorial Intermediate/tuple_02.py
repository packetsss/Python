a_tuple = ("Jack",) # or with out the parathesis
# print(a_tuple)

b_tuple = tuple(["Max", 28, "Unemployed"])
# print(b_tuple)
b = b_tuple[1:] # can use all lists properties (step: [2::], [::-1])
# print(b)

# for i in b_tuple: # print term by term
    # print(i)

# if "Max" in b_tuple:
#     print("T")

c_tuple = ("a", "d", "b", "c", "d")
# print(len(c_tuple))
# print(c_tuple.count("a")) # 0 will be returned if not included in the tuple e.g. "o"
# print(c_tuple.index("d")) # first occurance of d
list(c_tuple) # change to list
tuple(c_tuple) # change it back to tuple

i1, *i2, i3 = c_tuple
print(i1) # first item
print(i3) # last item
print(i2) # all items in the middle(list)

# list is larger than tuple,
# tuple is easier to iterate, more efficient
# takes longer to create list


