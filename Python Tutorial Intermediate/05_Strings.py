# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

str1 = "I like\nbeing goof"
str2 = "I like \
being goof"
'''print(str2)'''
# add a line or continue in a same line

which_character = str1[2:-1]
'''print(which_character)'''
# shows the character in designated spot

which_character = str1[::-1]
'''print(which_character)'''
# reverse, [::2] takes every two character

tot = str1 + " " + str2
'''print(tot)'''
# add two strings together

'''for i in tot:
    print(i)'''
# obtain character letter in tot

# can use if to check 

str3 = "   okay boi   "
'''print(str3.strip())'''
# removes empty spaces

str1.startswith("I")
str1.endswith("I")
# ...

str1.find("I")
# check the first index, if not find return -1

str1.count("I")
# ...

b = str1.replace("I", "Aj")
'''print(b)'''
# ...

a_list = str1.split()
'''print(a_list)'''
# splits the string into lists by looking at spaces(or whatever in the ())

a_str1 = " ".join(a_list)
'''print(a_str1)'''
# turn list back to string, join every element in the list by "whatever"

from timeit import default_timer
b_list = ["c"] * 30000

start = default_timer()
b_str = " ".join(b_list)
stop = default_timer()
'''print(stop-start)'''
# good way

'''start = default_timer()
b_str = " "
for i in b_list:
    b_str += i
stop = default_timer()
print(stop-start)'''
# bad way to convert list to str, takes longer. good way is above

c_variable = "Tompson"
c_str = "The var is %s" % c_variable
'''print(c_str)'''
# % is a place holder: string is %s, number is %d, float is %f
d_variable = 3.14159
d_variable1 = 22
d_str = "The var is {:.2f} and {}".format(d_variable, d_variable1)
'''print(d_str)'''
# :.2f is 2 digits after the decimal point

d_str = f"The var is {d_variable:.2f} and {d_variable1*2}"
print(d_str)
# best way, f string


