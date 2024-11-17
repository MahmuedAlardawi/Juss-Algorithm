import pandas as pd

# Load the evaluation results from the CSV file
evaluation_file_path = 'ALLaM_evaluation_output/RAG_evaluation_results.csv'
eval_results = pd.read_csv(evaluation_file_path)

# Display the first few rows of the DataFrame
print("First few rows of the evaluation results:")
print(eval_results.head())

# Summary statistics of the evaluation metrics
print("\nSummary statistics:")
print(eval_results.describe())