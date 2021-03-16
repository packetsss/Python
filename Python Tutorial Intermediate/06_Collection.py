from collections import Counter

a = "aaasdafffqqewawweejjjkkk"
a_counter = Counter(a)
print(a_counter.items())
# count how many times a letter appears and store as a dictionary

'''print(a_counter.keys())'''
# check dictionary keys

'''print(a_counter.most_common(1)[0][0])'''
# output: [('a', 5)]. (1) is the most common, 
# first [0] is the first element in the list: ('a', 5), 
# second [0] is the first element in the tuple: a

'''print(list(a_counter.elements()))'''
# get iterable elements in a list, sorted from most frequent

from collections import namedtuple
a_2d_point = namedtuple("Point", "x, y")
a = a_2d_point(3, -9)
'''print(a)'''
# show point x = 3 and y = -9
'''print(a.x, a.y)'''
# access the appointed value

from collections import OrderedDict
# same order, for older version

from collections import defaultdict
d = defaultdict(int) # appointed default type, return 0 in not found(not ane error)
d['a'] = 1
d['b'] = 2
'''print(d["a"])'''
# access the dictionary

from collections import deque
d = deque()

d.append(1)
d.appendleft(2)
d.pop()
d.extendleft([4, 5, 6]) # add 6, 5, 4 to the left
d.rotate(1) # move all to right 1 place
'''print(list(d))'''
# turn deque to list

