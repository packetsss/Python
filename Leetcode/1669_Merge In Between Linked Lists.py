list1 = [0, 1, 2, 3, 4, 5, 6]
a = 2
b = 4
list2 = [1000000, 1000001, 1000002, 1000003, 1000004]

counter1 = 0
counter2 = 0
for i in list1:
    if i == a:
        counter2 = counter1
        # print(counter2)
        for j in list1[counter1:]:
            if j == b:
                list1[counter1:counter2 + 1] = []
                # print(list1[counter1:counter2])
                break
            counter2 += 1
            # print(counter2)
        # list1.insert(counter1, list2)
        list3 = list1[:counter1] + list2 + list1[counter1:]
        break
    counter1 += 1

print(list3)

# I don't know what list node is???
