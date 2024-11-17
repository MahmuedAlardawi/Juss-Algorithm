import json
import os
from ragas import EvaluationDataset, evaluate
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, SemanticSimilarity
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from datasets import Dataset
import pandas as pd

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = ""
# Initialize the evaluator LLM using gpt-4o
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

# Load the evaluation dataset from a JSON file
# The JSON file should have keys: user_input, retrieved_contexts, generated_answer, reference
# Load JSON data
with open("ALLaM_evaluation_output/RAG_evaluation_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Convert the list of dictionaries to a DataFrame
data_df = pd.DataFrame(data)

# Convert the DataFrame to a Hugging Face Dataset
hf_dataset = Dataset.from_pandas(data_df)

# Create an EvaluationDataset from the Hugging Face Dataset
eval_dataset = EvaluationDataset.from_hf_dataset(hf_dataset)

# Define the evaluation metrics
metrics = [
    LLMContextRecall(llm=evaluator_llm),
    FactualCorrectness(llm=evaluator_llm),
    Faithfulness(llm=evaluator_llm),
    SemanticSimilarity(embeddings=evaluator_embeddings)
]
results = evaluate(dataset=eval_dataset, metrics=metrics)

# Convert results to a Pandas DataFrame
df = results.to_pandas()

# Display the first few rows of the DataFrame
print(df.head())

# Save the evaluation results to a CSV file
evaluation_file_path = "ALLaM_evaluation_output/RAG_evaluation_results.csv"
df.to_csv(evaluation_file_path, index=False)
print(f"Evaluation results saved to {evaluation_file_path}")
