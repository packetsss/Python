# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import copy

# shallow copy: only one level deep
org = [0, 1, 2, 3, 4]
cpy = copy.copy(org)
# didn't affect original

cpy1 = org.copy()
# also works

cpy2 = org[:]
# also works
cpy[2] = 10
'''print(org)
print(cpy)
'''

org = [[0, 1, 2, 3, 4], [5, 6, 7]]
cpy = copy.copy(org)
cpy[0][0] = 10
'''print(org)
print(cpy)'''
# doesn't work in the list of the list
# only one level deep: shallow copy

cpy = copy.deepcopy(org)
# deep copy works for all levels


class person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class company:
    def __init__(self, boss, employee):
        self.boss = boss
        self.employee = employee


p1 = person("Alex", 27)
p2 = person("Joe", 5)

company11 = company(p1, p2)
company11_clone = copy.copy(company11)
company11_clone.boss.age = 50

print(company11_clone.boss.age)
print(company11.boss.age)
# got affected since age is at lvl 2
# use deepcopy to avoid this

