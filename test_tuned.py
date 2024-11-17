import json
import os

from ALLaM_Tuned import Tuned

# Initialize QuestionFormatter with the access token
tuned = Tuned()

# Define poem titles and parameters
poem_titles = [
    "حب ليلى",
    "شوق الأندلس",
    "وداع المحبوب",
    "أمل الغد",
    "دموع الفراق",
    "نصر المجاهد",
    "رثاء الوطن",
    "حلم الشباب",
    "غروب الشمس",
    "بداية الربيع"
]
meter = 'طويل'  # Meter of the poem

all_responses = []
for title in poem_titles:
    # Define the question and get the response
    response = tuned.get_response(title, 22, meter)
    all_responses.append(response)

# Save all responses to a JSON file
output_dir = "ALLaM_fineTuned_output"
os.makedirs(output_dir, exist_ok=True)
file_path = f"{output_dir}/generated_poems.json"

with open(file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_responses, json_file, ensure_ascii=False, indent=4)

print(f"\nAll poems saved to {file_path}")