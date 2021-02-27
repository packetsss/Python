'''@mydecorator
def do_something():
    pass'''
# being extended by @mydecorator

import functools


def start_end_decorator(func):
    @functools.wraps(func)  # in order to show the correcct function name
    def wrapper(*args, **kwargs):
        # *args, **kwargs allows wrapper to take multiple arguments(* accepts positional arguments, ** accepts keywords)
        print("Start")
        a = func(*args, **kwargs)
        print("End")
        return a  # needs to store the variable in order to print the result

    return wrapper


# templete for a decorator

def print_name():
    print("ALex")


print_name = start_end_decorator(print_name)
'''print_name()'''


# run function inside another function

@start_end_decorator
def print_name1():
    print("ALex")


'''print_name1()'''


# same output using decorator method

@start_end_decorator
def add_5(x):
    return x + 5


'''result = add_5(10)'''
'''print(result)'''


def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator_repeat


# way to use decorators with arguments

@repeat(num_times=4)
def greeting(name):
    print(f"Hello {name}")


'''greeting("Aj")'''


# repeat name 4 times


def start_end_decorator1(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Start")
        a = func(*args, **kwargs)
        print("End")
        return a

    return wrapper


def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__!r}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {result!r}")
        return result

    return wrapper


@debug  # first execute
@start_end_decorator1  # execute inside debug
def hello(name):
    greeting = f"Hello {name}"
    print(greeting)
    return greeting


'''hello("Alex")'''


# execute multiple decorators

class count_times:

    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"This is executed {self.num_calls} times")
        return self.func(*args, **kwargs)


@count_times
def say_hello():
    print("Hello")


say_hello()
say_hello()
# every time we run it calculates the time


