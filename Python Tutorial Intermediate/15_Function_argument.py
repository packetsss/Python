def foo(a, b, c, d=4):
    print(a, b, c, d)


'''foo(1, b=2, c="aj")'''
# keyword argument doesn't matter sequence, can use a positional argument before a keyword argument
# take default value for d, can change to another. can't assign between positional arguments


def foo1(a, b, *o, **oo):
    print(a, b)
    for ar in o:
        print(ar)
    # prints the additional numbers in a new line
    for k in oo:
        print(k, oo[k])
    # prints the additional keywords and the value


'''foo1(1, 2, 3, 4, 5, 6, six=7)'''


def foo2(a, b, *, c, d):
    # must take keyword arguments after the *
    print(a, b, c, d)


'''foo2(1, 3, c=4, d=5)'''


def foo3(*args, last):
    # enforce keyword only arguments
    for a in args:
        print(a)
    print(last)


'''foo3(2, 5, 3, 7, last=0)'''


def foo4(a, b, c):
    print(a, b, c)


my_list = [0, 1, 2]
'''foo4(*my_list)'''
# * unpack the list into function, length must match(same)

my_dict = {"a": 1, "b": 2, "c": 3}
f'''oo4(**my_dict)'''
# ** unpack the dictionary into the function, keyword and length must match


def foo5():
    global num
    x = num
    num = 2
    # make num variable not local: global
    print(f"# inside the func: {x}")


num = 0
'''foo5()
print(num)'''
# prints out the modified num


def foo6(x):
    x = 5


var = 10
foo6(var)
# can't change var to x since integer is immutable
'''print(var)'''


def foo7(list_1):
    """list_1 = [0, 0, 0]"""
    # will rebind this list within the function, can't access global obj anymore
    '''list_1 += [0, 0, 0]'''
    # this is the right way to add
    list_1.append(4)
    list_1[1] = 100


listsss = [1, 3, 5]
foo7(listsss)
# mutable object can be changed: lists, immutable obj in mutable objs can also be changed
'''print(list_1)'''

