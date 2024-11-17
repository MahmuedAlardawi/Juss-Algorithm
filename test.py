# Load the data from the minimized JSON file and calculate the number of entries and total number of poem lines
import json

import pandas as pd

minimized_file_path = 'ALLaM_training_data_filtered_minimized_2.json'

with open(minimized_file_path, 'r', encoding='utf-8') as file:
    minimized_data = json.load(file)

# Calculate the total number of entries and total number of lines of poems
total_entries = len(minimized_data)
total_poem_lines = sum(len(entry['output'].split('\n')) for entry in minimized_data)

print('Total Data Entries:', total_entries, '\nTotal Poem Verse Line:', total_poem_lines)

df = pd.DataFrame(minimized_data)
print(df.head(10))