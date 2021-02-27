friends = ["Jake", "Jack", "Jacky", 3, True]

print(friends)
print(friends[4])
print(friends[1:4])
friends[2] = "Monk"
print(friends[2])

Lucky_numbers = [3, 2, 6, 754, 24, 75, 294, 2055]

friends.extend(Lucky_numbers)
friends.append("aj")
friends.insert(2, "goofy")
friends.remove("Jack")
print(friends)

friends.pop()
print(friends)

print(friends.index("Jake"))

friends.clear()
print(friends)

friend = ["aj ", "bj ", "bj ", "cj, ", "dj", "bj "]
friend.sort()
print(friend)
Lucky_numbers.sort()
print(Lucky_numbers)
Lucky_numbers.reverse()
print(Lucky_numbers)

friend3 = friend.copy()
print(friend3)
