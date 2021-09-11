a_tuple = (1, 12) # or with out the parathesis
#print(a_tuple)

b_tuple = tuple(["Max", 28, "Unemployed", 2.0])
#print(b_tuple)
b = b_tuple[:2] # can use all lists properties (step: [2::], [::-1])
#print(b)

#for i in b_tuple: # print term by term
#    print(i)

#if "Max" in b_tuple:
#    print(True)

c_tuple = ("a", "b", [1, 2], [3, 4])
#print(len(c_tuple))
#print(c_tuple.count("a")) # 0 will be returned if not included in the tuple e.g. "o"
#print(c_tuple.index("d")) # first occurance of d
list(c_tuple) # change to list
tuple(c_tuple) # change it back to tuple

#a, b, *c = c_tuple
#print(a) # first item
#print(b) # last item
#print(c) # all items in the middle(list)

# list is larger than tuple,
# tuple is easier to iterate, more efficient
# takes longer to create list


