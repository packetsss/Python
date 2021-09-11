a_dictionary = {
                "name": "Mark", 
                "age": 30, 
                "city": "Irvine"
                }
#print(a_dictionary)

b_dictionary = dict(name="Mark", age=30, city="Irvine")
# both ways to create dictionary

#print(a_dictionary["age"])
# use dictionary

a_dictionary["email"] = "123@gmail.com"
#a_dictionary[1] = 2
#a_dictionary.update({"email": "123", "2": 2})
#a = {"email": "123", "2": 2}
#c = {**a, **a_dictionary, 1: 66}
#print(c)
# add a value to dictionary

a_dictionary["email"] = "888888@gmail.com"
# change value

#del a_dictionary["name"]
#a_dictionary.pop("name")
# both ways to delete a value

'''try:
    print(a_dictionary["nameff"])
except:
    print("Error")'''

a_dictionary.keys()
print(list(a_dictionary.items()))
a_dictionary.values()
# get the key or the value

for a, b in a_dictionary.items():
    print(a, b)
# print out all keys and values

c_tuple = (3, 7)
c_dictionary = {c_tuple: 15}
print(c_dictionary)
# use tuple as a key(can't use list)

