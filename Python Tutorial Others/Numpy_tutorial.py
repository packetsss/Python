# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import numpy as np

a = np.array([1, 2, 3])
# numpy list

b = np.array([[9.0, 8.0, 7.0], [6.0, 5.0, 4.0]])
'''print(b)'''
# 2d array

'''print(b.ndim)'''
# get dimension

'''print(a.shape)'''
# get # of elements in 1st, 2nd... dimension

'''print(a.dtype)'''
# int32 by default
# a = np.array([1, 2, 3], dtype="int16") to change type

'''print(a.itemsize)'''
# int 32 have size of 4

'''print(a.size * a.itemsize)
or
print(a.nbytes)'''
# total size


c = np.array([[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14]])

'''print(c[0, 2] == 3)'''
# get specific element

'''print(c[0, :])'''
# get whole 1st row

'''print(c[0, 1:-1:2])'''
# step the array

c[1, 5] = 20
'''print(c)'''
# change element

c[:, 2] = [1, 2]
# change all 2nd cln to 5

d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
'''print(d)'''
# 3d array

'''print(d[0, 1, 1])'''
# index for 4

d[:, 1, :] = [[9, 9], [8, 8]]
# replace value


e = np.zeros((5, 3, 4))
'''print(e)'''
# get multidimensional zeros matrix

f = np.ones(3)
'''print(f)'''
# get all ones

'''print(np.full((2, 2), 99))'''
# get all 99's

'''print(np.full_like(c, 4))'''
# get all 4's using c's dimension

'''print(np.random.rand(4, 2))
print(np.random.random_sample(c.shape))'''
# random from 0 to 1 using given size

'''print(np.random.randint(1, 5, size=(3, 3)))'''
# get a randi matrix from 2 to 4

'''print(np.identity(5))'''
# identity matrix

arr = np.array([[1, 2, 3]])
r1 = np.repeat(arr, 3, axis=0)
'''print(r1)'''
# repeat arr 3 times


quiz = np.zeros((9, 9))
quiz[0, :] = 1
quiz[:, 0] = 1
quiz[-1, :] = 1
quiz[:, -1] = 1
dim = int(np.floor(quiz.shape[0] / 2))

quiz[dim, dim] = 9
'''print(quiz)'''

g = np.array([1, 2, 3, 4])
'''print(g+2)'''
# add every element by 2

g * 2
g - 2
g ** 3
np.sin(g)
# all calculation

h = np.array([1, 0, 1, 0])
'''print(g + h)'''
# array add array


a1 = np.ones((2, 3))
b1 = np.full((3, 2), 2)
'''print(np.matmul(a1, b1))'''
# matrix multiplication

c1 = np.identity(3)
'''print(np.linalg.det(c1))'''
# identity matrix has a det of 1


stats = np.array([[1, 2, 3], [4, 5, 6]])
'''print(np.min(stats), np.max(stats, axis=1), np.sum(stats, axis=0))'''
# axis 1 is the most row, axis 0 is the most column

'''print(stats.reshape((3, 2)))'''
# change rows to clns, clns to rows

stack = np.vstack([a, stats, stats])
'''print(stack)'''
# join multiple matrix together, vertical stack

'''print(np.hstack([stats, stats]))'''
# horizontal stack


tx = np.genfromtxt("data_np.txt", delimiter=",")
# get all data from txt separated by a comma

tx1 = tx.astype("int32")
# change float type to int32

s = (tx1 > 50)
ss = (~((tx1 > 50) & (tx1 < 100)))
# get a boolean array of trues and falses
# ~ is not

gtfy = tx1[tx1 > 50]
# all values greater than 50

'''print(g[[1, 3]])'''
# index multiple elements

any1 = np.any(tx1 > 50, axis=0)
'''print(any1)'''
# return a row vector of any elements in all clns > 50, can use all as well

ee = np.array([1, 2, 3, 4, 5])
exam = np.array([ee, ee+5, ee+10, ee+15, ee+20, ee+25])
'''print(exam)'''

# qt1
'''print(exam[2:4, 0:2])'''

# qt2
'''print(exam[[0, 1, 2, 3], [1, 2, 3, 4]])'''

# qt3
'''print(exam[[0, 4, 5], 3:])'''


# Numpy dot product: np.dot(arr1, arr2)


