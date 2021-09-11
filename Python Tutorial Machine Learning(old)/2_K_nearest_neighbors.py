# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import sklearn
from sklearn import linear_model, preprocessing
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np

"""
Find K amount of points closest to the picked point, and then pick the highest occurrence of a group in this K range,
and then predict the picked point is in that group

K needs to be an odd number in order to have a winner group

Distance is the magnitude
"""

data = pd.read_csv("src\\car.data")
print(data.head())

le = preprocessing.LabelEncoder()
buying = le.fit_transform(list(data["buying"]))
maint = le.fit_transform(list(data["maint"]))
door = le.fit_transform(list(data["door"]))
persons = le.fit_transform(list(data["persons"]))
lug_boot = le.fit_transform(list(data["lug_boot"]))
safety = le.fit_transform(list(data["safety"]))
cls = le.fit_transform(list(data["class"]))

# print(buying)
# Numpy array: vhigh --> 3, low --> 1

X = list(zip(buying, maint, door, persons, lug_boot, safety))
y = list(cls)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)

# print(x_train, y_test)
# convert the data to list of tuples

model = KNeighborsClassifier(n_neighbors=9)

model.fit(x_train, y_train)
acc = model.score(x_test, y_test)
print(acc)

predicted = model.predict(x_test)
names = ["un_acc", "acc", "good", "very_good"]

for x in range(len(predicted)):
    print(f"Predicted: {names[predicted[x]]}, Data: {x_test[x]}, Actual: {names[y_test[x]]}")
    n = model.kneighbors([x_test[x]], 9, True)
    print(f"N: {n}")
