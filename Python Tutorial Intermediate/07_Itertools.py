# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from itertools import product

a = [1, 2]
b = [3, 4]
prod = product(a, b, repeat=2)
'''print(list(prod))'''
# cross combine 2 lists, repeat is allow to repeat

from itertools import permutations

a = [1, 2, 3]
perm = permutations(a, 4)
'''print(list(perm))'''
# show all possible arrangements in a list, second peremeter is to specify the length(return empty list if exceed)

from itertools import combinations, combinations_with_replacement

a = [1, 2, 3, 4]
comb = combinations(a, 2)
'''print(list(comb))'''
# show all possible combinations in a list with certain length(2)(no repeat it self)

comb_wr = combinations_with_replacement(a, 2)
# with repeat

from itertools import accumulate

a = [1, 2, 3, 4]
acc = accumulate(a)
'''print(list(acc))'''
# every term accumulates by adding all before terms: 1 = 1, 2 = 1 + 2, 3 = 1 + 2 + 3
import operator

acc = accumulate(a, func=operator.mul)  # mul = multiply, max: replace all value after the max value in the list
# every term accumulates by multipling all before terms

from itertools import groupby


def smaller_than_three(x):
    return x < 3


a = [1, 2, 3, 4]
group_obj = groupby(a, key=smaller_than_three)
'''for key, value in group_obj:
    print(key, list(value))'''
# for nums < 3 in list a, return true, otherwise false

group_obj = groupby(a, lambda x: x < 3)
'''for key, value in group_obj:
    print(key, list(value))'''
# same thing as above

persons = [
    {"name": "Mark", "age": 65, "city": "Iron"},
    {"name": "Hop", "age": 10, "city": "Kioq"},
    {"name": "Quuin", "age": 33, "city": "Jafferson"}
]

group_obj = groupby(persons, lambda x: x["age"])
'''for key, value in group_obj:
    print(key, list(value))'''
# age gets pulled out front

from itertools import count, cycle, repeat

'''for i in count(100):
    print(i)'''
# infinitly adding up 100's

a = [1, 2, 3]
'''for i in cycle(a):
    print(i)'''
# infinitly cycle through the list

'''for i in repeat(1, 3):
    print(i)'''
# infinitly loop to print 1; second argument specifies the repeat times
