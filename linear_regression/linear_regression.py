import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.linear_model
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


def prepare_data(white_wine):
    return white_wine[["alcohol", "residual sugar"]].iloc[:]


# Load the data
white_wine = pd.read_csv("winequality-white.csv", sep=';')

# Prepare the data
data = prepare_data(white_wine)
X = np.c_[data["alcohol"]]
y = np.c_[data["residual sugar"]]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Visualize the data
data.plot(kind='scatter', x="alcohol", y='residual sugar')
plt.show()

# Select a linear model
model = sklearn.linear_model.LinearRegression()

# Train the model
r = model.fit(X_train, y_train)

# Make a prediction for Cyprus
X_new = [[9.8]]
print(model.predict(X_new))

# Calculate loss
y_pred = model.predict(X_test)
loss = mean_absolute_error(y_test, y_pred)
print(loss)
