import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Step 1: Load the dataset (must be in the same folder)
df = pd.read_csv("SOCR-HeightWeight.csv")

# Step 2: Extract features (Height) and target (Weight)
X = df[['Height(Inches)']]  # input feature
y = df[['Weight(Pounds)']]  # target value

# Step 3: Train the model
model = LinearRegression()
model.fit(X, y)

# Step 4: Save the trained model
with open("final_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as final_model.pkl")
