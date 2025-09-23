import pandas as pd

# Load the results file
df = pd.read_csv('model_evaluation_results.csv')

# Display the results
print("\n📊 Model Evaluation Results:\n")
print(df)
