# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

a_set = {2, 6, 7, 2}
'''print(a_set)'''
# set does not allow duplicate

b_set = set("hello")
'''print(b_set)'''
# sets are unordered

c_set = set()
# get a empty set

a_set.add(3)
a_set.remove(7)
a_set.discard(2)
'''print(a_set)'''
# add and remove

odd_set = {9, 7, 5, 3, 1}
even_set = {0, 2, 8, 6, 4}
union = odd_set.union(even_set)
'''print(union)'''
# union added a reordered the 2 sets

even_set.add(1)
inters = odd_set.intersection(even_set)
'''print(inters)'''
# find any intersection

diff = odd_set.difference(even_set)
'''print(diff)'''
# find nums in odd_set that even_set doesn't have

sym_diff = odd_set.symmetric_difference(even_set)
'''print(sym_diff)'''
# find nums that doesn't exist in both sets

'''odd_set.update(even_set)'''
# updates the odd_set: can use intersection_update, difference_update, symmetric_difference_update

odd_set.issubset(even_set)
# even_set contains odd_set
odd_set.issuperset(even_set)
# opposite

even_set.remove(1)
'''print(odd_set.isdisjoint(even_set))'''
# both sets have nothing in common

odd_set1 = odd_set.copy()
odd_set1.add(2)
'''print(odd_set1)
print(odd_set)'''
# copy a set

frzset = frozenset([2, 4, 6, 1])
# immutable set

f1 = frzset.union(odd_set)
print(f1)
# union, inters, dif will work