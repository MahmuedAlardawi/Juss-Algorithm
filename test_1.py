import json
import re

def process_file_with_line_count_update(input_file_path, output_file_path):
    # Load the data from the input file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Filter and process the entries
    filtered_data = []
    for entry in data:
        output_lines = entry['output'].split('\n')
        num_lines = len(output_lines)

        if num_lines == 22:
            # Replace the line count in 'input' string with the new number of lines
            entry['input'] = re.sub(r'من \d+ أشطار', f'من {num_lines} أشطار', entry['input'])
            filtered_data.append(entry)
        elif num_lines > 22:
            # Truncate the output and update the input line count to 22
            entry['output'] = '\n'.join(output_lines[:22])
            entry['input'] = re.sub(r'من \d+ أشطار', 'من 22 أشطار', entry['input'])
            filtered_data.append(entry)

    # Save the cleaned data to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(filtered_data, output_file, ensure_ascii=False, indent=2)

    return output_file_path

# File paths
input_file_path = 'ALLaM_training_data_filtered_minimized.json'
output_file_path = 'ALLaM_training_data_filtered_minimized_1.json'

# Call the function
process_file_with_line_count_update(input_file_path, output_file_path)