# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

def my_generator():
    yield 1
    yield 10
    yield 2


g = my_generator()

'''for i in g:
    print(i)'''
# prints each value in my_g

'''value = next(g)
print(value)
value = next(g)
print(value)'''
# run and pauses at the first line, and second line... if exceed cause StopIteration

'''print((sum(g)))'''
# sum up all values

'''print(sorted(g))'''
# sort it out


def count_down(num):
    print("starting")
    while num > 0:
        yield num
        num -= 1


cd = count_down(4)

'''value = next(cd)
print(value)
print(next(cd))
print(next(cd))
print(next(cd))'''
# execution of generators


def first_to_n(n):
    nums = []
    num = 0
    while num < n:
        nums.append(num)
        num += 1
    return nums


'''print((first_to_n(10)))
print(sum(first_to_n(10)))'''
# takes a lot of memory while executing it


def first_to_n_generator(n):
    num = 0
    while num < n:
        yield num
        num += 1


'''print(sum(first_to_n_generator(10)))'''
# don't need to save all values in the list


def fibonacci(limit):
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b


fib = fibonacci(20000)
'''for i in fib:
    print(i)'''
# the way to calculate fibonacci sequence


my_generator1 = (i for i in range(10) if i % 2 == 0)
print(list(my_generator1))
'''for i in my_generator1:
    print(i)'''
# saves memory than list: [i for i in range(10) if i % 2 == 0]
