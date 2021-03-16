# *******

res = 1 * 2
# multiplication

res1 = 2 ** 4
# power

zeros = [0] * 10
zeros1 = "AB" * 10
'''print(zeros1)'''
# create a list 10 times

# *args, **kwargs
# unpack lists, dictionary

nums = [1, 2, 3, 4, 5, 6]
*beginning, last = nums
# unpack last value, always unpack to a list even given tuple
'''beginning, * last = nums'''
# will unpack the first value
'''beginning, *middle, second_last, last = nums'''
# will unpack beginning, second_last, and last
'''print(beginning)
print(last)'''

tuple1 = (1, 2, 3)
list1 = [4, 5, 6]
set1 = {7, 8, 9}

new_list = [*tuple1, *list1, *set1]
'''print(new_list)'''
# merge lists, tuples, and sets into a list

dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
new_dict = {**dict1, **dict2}
'''print(new_dict)'''
# merge 2 dictionaries




