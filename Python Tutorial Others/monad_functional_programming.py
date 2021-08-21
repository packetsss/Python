#%%
import time
from operator import neg
#%%
"""
`int` will throw a ValueError exception because it can't convert that string to an integer value. We will end up in an exception handler somewhere else in our code, or worse still our program might terminate with an error message. This is exactly the sort unpredictability the functional programming is supposed to solve.

Now imagine if the int function was able to return not only the integer value, but also a flag to say whether the conversion had succeeded or failed. This failed flag could be thought of as a context around the actual data - if the failed flag is false, the data is valid, if the failed flag is true we should ignore the data as it isn't valid.

- It makes composition of functions easier
- Avoid repeating computational patterns
- Useful when pipelining operations
"""
def fast(x):
    return x + 1

def slow(x):
    time.sleep(1)
    return x - 1

x = "XYZ"
y = slow(fast(int(x)))
y
# %%
class Failure():
    def __init__(self, value, failed=False):
        self.value = value
        self.failed = failed
    def get(self):
        return self.value
    def is_failed(self):
        return self.failed
    def __str__(self):
        return ' '.join([str(self.value), str(self.failed)])
    def __or__(self, f):
        return self.bind(f)
    def bind(self, f):
        if self.failed:
            return self
        try:
            x = f(self.get())
            return Failure(x)
        except:
            return Failure(None, True)
# %%
x = '1'
y = Failure(x).bind(int).bind(neg).bind(str)
print(y)

x = 'XYZ'
y = Failure(x).bind(int).bind(neg).bind(str)
print(y)
# %%
