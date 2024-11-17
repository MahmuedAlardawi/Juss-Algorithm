import pandas as pd

# Load the dataset
file_path = 'training_data.csv'  # Replace with the actual path to your CSV file
data = pd.read_csv(file_path)

# Drop rows with any NaN values
data = data.dropna()

total_rows = data.size

print("Total number of poems:", total_rows)
