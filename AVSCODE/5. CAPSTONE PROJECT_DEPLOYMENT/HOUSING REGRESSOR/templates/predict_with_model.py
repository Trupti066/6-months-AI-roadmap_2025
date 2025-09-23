import pandas as pd
import pickle

# Load the dataset again
data = pd.read_csv("USA_Housing.csv")
x = data.drop(['Price', 'Address'], axis=1)
x.columns = [col.replace(' ', '_') for col in x.columns]  # Fix column names
y = data['Price']

# Split into train/test again
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Load the saved model (change filename as needed)
with open('RandomForest.pkl', 'rb') as f:
    model = pickle.load(f)

# Predict on test data
predictions = model.predict(X_test)

# Show first 5 predictions
print("🔮 First 5 Predictions:")
print(predictions[:5])
