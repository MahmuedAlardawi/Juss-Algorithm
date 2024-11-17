import json
import re

def process_file_with_line_count_update(input_file_path, output_file_path):
    # Load the data from the input file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Filter and process the entries
    filtered_data = []
    for i in range(len(data)):
        output_lines = data[i]['output'].split('\n')
        num_lines = len(data[i])

        if i <= 5000:
            filtered_data.append(data[i])
        else:
            break

    # Save the cleaned data to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(filtered_data, output_file, ensure_ascii=False, indent=2)

    return output_file_path

# File paths
input_file_path = 'ALLaM_training_data_filtered_minimized_1.json'
output_file_path = 'ALLaM_training_data_filtered_minimized_2.json'

# Call the function
process_file_with_line_count_update(input_file_path, output_file_path)