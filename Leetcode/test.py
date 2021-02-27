# 1
'''x = 0

y = list(str(x))

if y != ["0"]:
    a = str(y[-1])
    while a == "0":
        y.pop(-1)
        a = str(y[-1])

x_list = y[::-1]
if "-" in x_list:
    x_list.remove("-")
    x_list = ["-"] + x_list

a = int("".join(x_list))
b = 2**31
if a <= b - 1 and a >= -b:
    print(a)
else:
    print(0)'''

# 2
'''num = [1, 6, 1, 1, 1]
list1 = []
times = 0
for i in num:
    times += 1
    i = sum(num[:times])
    list1.append(i)
print(list1)'''

# 3
'''stones = "abbdhCyuqcjmynaa"
jewels = "CajJf"
list1 = []
for i in jewels:
    list1.append(stones.count(i))
print(sum(list1))'''

# 4
'''accounts = [[1,2,3],[8,2,1]]
list1 = []
for i in accounts:
    list1.append(sum(i))
print(max(list1))'''

# 5
'''from collections import Counter
allowed = "ab"
words = ["ad","bd","aaab","baa","badab", "b"]
k = 0
for i in words:
    if set(i).issubset(set(allowed)):
        k += 1
print(k)'''

# 6
'''from itertools import combinations, combinations_with_replacement

arr = [7,3,7,3,12,1,12,2,3]

a = 5
b = 8
c = 1

comb = list(combinations(arr, 3))
# comb1 = list(comb)
count = 0
print(len(list((count for qq in comb if abs(qq[0] - qq[1]) <= a and abs(qq[1] - qq[2]) <= b and abs(qq[0] - qq[2]) <= c))))'''

# 7
from collections import Counter
import copy


def strong_password_checker(password):
    key1 = "abcdefghijklmnopqrstuvwxyz"
    key2 = "abcdefghijklmnopqrstuvwxyz".upper()
    key3 = "0123456789"
    key4 = ".!"
    counter = 0
    num1 = 0
    num2 = 0
    num3 = 0
    missing_checker = 0
    min_missing_digits = 0
    max_missing_digits = 0
    password_copy = list(copy.deepcopy(password))

    class edition:
        @staticmethod
        def replace():
            last_time = 0
            repeat_list = []
            while last_time < len(password_copy):
                sub_array_size = 3
                for i in range(last_time, len(password_copy)):
                    if password_copy[i] * 3 == password_copy[i:i + sub_array_size]:
                        password_copy[i+1] = missing_letter
                        repeat_list.append(password[i])
                        print(1)
                        last_time += 3
                        break
                    else:
                        last_time += 1
                        break

    if len(password) < 6:
        counter += 6 - len(password)
        min_missing_digits = 6 - len(password)
    if len(password) > 20:
        counter += len(password) - 20
        max_missing_digits = len(password) - 20
    # check length constrain

    for letter in password:

        if letter in key1:
            num1 = 0
            break
        else:
            num1 += 1
            missing_letter = letter
    if num1 != 0:
        counter += 1
        missing_checker += 1
        edition.replace()
    # check lower case

    for letter in password:

        if letter in key2:
            num2 = 0
            break
        else:
            num2 += 1
            missing_letter = letter
    if num2 != 0:
        counter += 1
        missing_checker += 1
        edition.replace()
    # check upper case

    for letter in password:

        if letter in key3:
            num3 = 0
            break
        else:
            num3 += 1
            missing_letter = letter
    if num3 != 0:
        counter += 1
        missing_checker += 1
        edition.replace()
    # check number

    '''for letter in password:
        if letter not in key1 + key2 + key3 + key4:
            counter += 1
            break
    # check other characters'''

    '''if int(list(sorted(Counter(password).values()))[-1]) > 2:
        counter += 1'''

    """sub_array_size = 6
    for i in range(len(password) - sub_array_size + 1):
        '''print(password[i:i + sub_array_size])
        print(password[i])'''
        if password[i] * 3 == password[i:i + sub_array_size - 3]:
            print(password[i] * 3)
        if password[i] * 6 == password[i:i + sub_array_size]:
            print(password[i] * 6)"""

    last_time = 0
    repeat_list = []
    # print(len(password))
    while last_time < len(password):
        sub_array_size = 3
        for i in range(last_time, len(password)):
            if password[i] * 3 == password[i:i + sub_array_size]:
                counter += 1
                repeat_list.append(password[i])

                last_time += 3
                break
            else:
                last_time += 1
                break
    # check repeating values

    '''repeat_list = []
    for i in list(sorted(Counter(password).values())):
        if i > 2:
            counter += 1
            repeat_list.append(i)'''


    repeat_len = len(repeat_list)
    print(f"key values are: {list(sorted(Counter(password).values()))}")
    print(f"Number of repeats: {repeat_len}")
    print(f"Number of missing cases: {missing_checker}")
    print(min_missing_digits)
    if repeat_len != 0:
        if missing_checker == 1:
            counter -= 1
            if min_missing_digits == 1:
                counter -= 1
            if min_missing_digits == 2:
                counter -= 2
        elif missing_checker == 2:
            if repeat_len >= 2:
                counter -= 2
            elif repeat_len == 1:
                counter -= 1
            if 0 < min_missing_digits < 3:
                counter -= 2
        elif missing_checker == 3:
            if repeat_len < 3:
                counter -= repeat_len
            else:
                counter -= 3
            if min_missing_digits == 1:
                counter -= 1
    else:

        if missing_checker == 1:
            if min_missing_digits == 1:
                counter -= 1
        elif missing_checker == 2:
            if 0 < min_missing_digits < 4:
                counter -= 2
        elif missing_checker == 3:
            if min_missing_digits == 1:
                counter -= 1
    # counter -= abs(missing_checker)

    print(f"Needed steps: {counter}, length of the password: {len(password)}")
    print(password_copy)


strong_password_checker("..aaa.aaaa")
