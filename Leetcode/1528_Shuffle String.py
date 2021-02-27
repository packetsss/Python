s = "codeleet"
indices = [4,5,6,7,0,2,1,3]


list1 = [1]*len(s)

for i in range(len(indices)):
    list1[indices[i]] = s[i]

print("".join(list1))
