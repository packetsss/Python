# syntax error: print(a)))
# exception error: even syntax is correct, it will cause a error while running: a = 6 + "5"(type error)
    # type error, import(module) not found error, name error(not defined), file not found error, value or index error(not in the list),
    # key error(not inside dictionary)

x = -5
'''if x < 0:
    raise Exception("x should be positive")'''
# force to raise a error message

'''assert(x >= 0), "x should be positive"'''
# assert a x value, if not met, prints out error message

try:
    a = 5 / 0
except:
    '''print("error input")'''
# program will continue to except block if try block errors
try:
    a = 5 / 0
except Exception as e:
 '''   print(e)'''
# prints the exact error message

try:
    a = 5 / 0
    b = 4 * "2"
except ZeroDivisionError as e:
    '''print(e)'''
# do something if it's zero division error
except TypeError as e:
    '''print(e)'''
# if not zero division, move on and do something if it's type error
else:
    print("everything fine")
# run if no error occur
finally:
    print("clean up...")
# runs always, usually to clean up

class value_too_high_error(Exception):
    pass

class value_too_low_error(Exception):
    def __init__(self, message, value):
        self.messahe = message
        self.value = value

def test_value(x):
    if x > 100:
        raise value_too_high_error("Value is too high")
    if x < 5:
        raise value_too_low_error("Value is too low", x)

try:
    test_value(2)
except value_too_high_error as e:
    print(e)
except value_too_low_error as e:
    print(e.message, e.value) # not working
# define own error

