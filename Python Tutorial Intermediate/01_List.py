# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

mylist = ["banana", "apple", "grape"]
# print(mylist)

mylist2 = mylist[-2]

# print(mylist2)

# for i in mylist:
#     print(i)

# if "apple" in mylist:
#     print("Y")
# else:
#     print("N")

mylist.append("AJ")
#print(mylist)

mylist.insert(1, "January")
#print(mylist)

item = mylist.pop(2)
#print(item, mylist)
#print(mylist)

item = mylist.remove("AJ")
# print(mylist)

item = mylist.clear()
#print(mylist)
#l = [1, 2]
#dic = {
#    1: l,
#}
#l.clear()
#print(dic[1])

num_list = [-1, 8, -100, 80, 70, 4, -20]
#num_list.sort()
# num_list.sort()
#print(num_list)

new_list = sorted(num_list)
#print(new_list)

a_list = [3, 1] * 4
#print(a_list)

b_list = num_list + a_list
#print(b_list)

c_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
c = c_list[:4]
c = c[::3]
#print(c)
c = c_list[2:]
# print(c)
c = c_list[:]
#c = c_list[1:len(c_list):2]
print(c)

mylist = ["banana", "apple", "grape"]
mylist_copy = mylist
mylist_copy.append("lemon")
print(mylist_copy + mylist)
# Use mylist_copy = mylist.copy() to make a copy
# Use mylist_copy = list(mylist) to make a copy
# Use mylist_copy = mylist[:] to make a copy


s = "b"

d_list = [1, 2, 3, 4, 5, 6]
d = [i * i + 1 for i in d_list] # Square the whole list

print(d)
d = list(map(lambda x: x ** 4 + 1, d_list))
print(d)

# print(d)

print(tuple(range(9)))