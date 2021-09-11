# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import random

a = random.random()
'''print(a)'''
# range from 0 to 1

a = random.uniform(2, 100)
'''print(a)'''
# range from 2 to 100

a = random.randint(1, 10)
'''print(a)'''
# interger

a = random.randrange(1, 10)
'''print(a)'''
# interger without upper bound

a =random.normalvariate(0, 1)
'''print(a)'''
# pick a number in standard distribution

a_list = list("ABCDEFG")
a = random.choice(a_list)
# choose a random letter from the list

a = random.sample(a_list, 2)
# pick unique 2 letters (no over lap like (a, a))

a = random.choices(a_list, k=3)
'''print(a)'''
# It can pick overlap letters

random.shuffle(a_list)
'''print(a_list)'''
# shuffles the list

'''random.seed(1)
print(random.random())
print(random.randint(1, 10))

random.seed(2)
print(random.random())
print(random.randint(1, 10))'''
# all random is the same with the same seed (reproduce data)

import secrets

a = secrets.randbelow(10)
'''print(a)'''
# random from 0 to 10, not included 10

a = secrets.randbits(4)
'''print(a)'''
# generate random number from 0 to 15(binary)

a_list = list("ABCDEFG")
a = secrets.choice(a_list)
# create not reproducible choice

