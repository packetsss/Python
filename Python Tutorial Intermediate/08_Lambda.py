# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

add_10 = lambda x: x + 10
'''print(add_10(5))'''
# define add_10 as certain execution and conduct x as 5

def add_10_func(x):
    return x + 10
# same as above

muult = lambda x,y: x * y
'''print(muult(2,7))'''
# define a multiply function

point2D = [(1,2), (15,1), (5, -1), (10 ,4)]
po_sort = sorted(point2D, key=lambda x: x[1])
# default sorted to first index, with key function, sorted to y index
def sort_to_y(x):
    return x[1]
# does the same

po_sort = sorted(point2D, key=lambda x: x[0] + x[1])
# sort the sum

# map(func,seq)
a = [1, 2, 3, 4, 5, 6]
b = map(lambda x: x * 2, a)
'''print(list(b))'''
# transforms each element using a function: times all by two in the list
c = [x*2 for x in a]
# same thing

# filter(func,seq)
b = filter(lambda x: x%2==0, a)
print(list(b))
# only get the even function, % is the reminder in the division
c = [x for x in a if x%2==0]
# same thing

# reduce(func,seq)
from functools import reduce
product_a = reduce(lambda x,y: x * y, a)
'''print(product_a)'''
# multiply all the values in the list: 1*2=2*3=6*4=...
