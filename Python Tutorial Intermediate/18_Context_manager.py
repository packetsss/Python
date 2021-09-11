# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

"""with open('notes.txt', 'w') as f:
    f.write('some to do...')"""
# good way to access a file( don't need to close

"""f = open('notes.txt', 'w')
try:
    f.write('some todo...')
finally:
    f.close()"""


# redundant way


class ManagedFile:
    def __init__(self, filename):
        print('I\'m in it:', filename)
        self.filename = filename

    def __enter__(self):
        print('enter')
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.file:
            self.file.close()
        if exc_type is not None:
            print('Exception has been handled')
        # the way to handle exception
        print('exit')
        return True


with ManagedFile('notes.txt') as f:
    print('doing stuff...')
    '''f.write('some to do...')'''
    f.somemethod()
print("Continuing")
# implementing a context manager as a class

from contextlib import contextmanager


@contextmanager
def open_managed_file(filename):
    f1 = open(filename, 'w')
    try:
        yield f1
    finally:
        f1.close()


with open_managed_file('notes.txt') as f:
    '''f.write('some to do...')'''
# easier way to call a function using a with statement
