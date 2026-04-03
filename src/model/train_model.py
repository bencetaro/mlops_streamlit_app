import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

"""
In this demo project I use synthetic data to train a simple linear regression model for mimicking housing price prediction.
1. The script generates the data,
2. Trains a model,
3. Evaluates the model on a validation set,
4. Saves the trained model and the test set for later use in an API.
"""

np.random.seed(42)

size = np.random.randint(20, 200, 400)
# "n_rooms" feature based on "size", with some randomness
n_rooms = np.random.randint(1, 5, 400)
n_rooms[(size >= 20) & (size < 50)] = np.random.randint(1, 3, size[(size >= 20) & (size < 50)].shape[0])
n_rooms[(size >= 50) & (size < 100)] = np.random.randint(2, 4, size[(size >= 50) & (size < 100)].shape[0])
n_rooms[(size >= 100) & (size < 150)] = np.random.randint(3, 5, size[(size >= 100) & (size < 150)].shape[0])
n_rooms[(size >= 150) & (size <= 200)] = np.random.randint(4, 6, size[(size >= 150) & (size <= 200)].shape[0])
# "price" feature based on "size" and "n_rooms", with some randomness
price = size * 3000 + n_rooms * 50000 + np.random.normal(0, 20000, 400)
# "quality" feature based on price, with some randomness
quality = np.where(price < 100000, 3, np.where(price < 300000, 2, 1))
quality = np.where((size < 50) & (quality == 1), 2, quality)
quality = np.where((size > 150) & (quality == 3), 2, quality)

data = {
    "size": size,
    "price": price,
    "n_rooms": n_rooms,
    "quality": quality
}

df = pd.DataFrame(data)

train_df = df.sample(frac=0.6, random_state=42)
temp_df = df.drop(train_df.index)
valid_df = temp_df.sample(frac=0.75, random_state=42)
test_df = temp_df.drop(valid_df.index)
# print(len(train_df), len(valid_df), len(test_df))

X_train, y_train = train_df.drop(columns=["price"]), train_df["price"]
X_valid, y_valid = valid_df.drop(columns=["price"]), valid_df["price"]

# Train
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate 
y_pred = model.predict(X_valid)
mse = np.mean((y_valid - y_pred) ** 2)
print(f"Validation MSE: {mse:.2f}")

# Save model, and test set
os.makedirs("output", exist_ok=True)
joblib.dump(model, "output/model.pkl")
test_df.drop(columns=["price"], inplace=True)
test_df.to_csv("output/test_set.csv", index=False)
print("Model saved!")
