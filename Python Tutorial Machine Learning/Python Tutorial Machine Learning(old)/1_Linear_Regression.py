import pandas as pd
import numpy as np
import tensorflow
import keras
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as pyplot
from matplotlib import style
import pickle

data = pd.read_csv("src\\student-mat.csv", sep=";")
# csv --> comma separated valuers
data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]

predict = "G3"
# labels, what I'm trying to get
X = np.array(data.drop([predict], 1))
y = np.array(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)
# splitting 10% of data in test sample

'''# linear Regression: attempt to draw best fit line in a 2D or 3D graph(data needs to be correlate to each other)
linear = linear_model.LinearRegression()
linear.fit(x_train, y_train)
accuracy = linear.score(x_test, y_test)
# about 0.8 accuracy

print(f"Co: {linear.coef_}\nIntercept: {linear.intercept_}")

# with open("src\\studentmodel.pickle", "wb") as f:
#     pickle.dump(linear, f)'''

with open("src\\studentmodel.pickle", "rb") as f:
    linear = pickle.load(f)

predictions = linear.predict(x_test)
for x in range(len(predictions)):
    print(predictions[x], x_test[x], y_test[x])

p = "studytime"
style.use("ggplot")
pyplot.scatter(data[p], data["G3"])
pyplot.xlabel(p)
pyplot.ylabel("Final Grade")
pyplot.show()
