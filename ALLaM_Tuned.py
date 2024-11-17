import requests
import json
import os
from datetime import datetime

class Tuned:
    def __init__(self):
        pass

    @staticmethod
    def construct_prompt(poem_title, num_lines, meter):
        # Construct the input prompt for generating a poem with specific constraints, including diacritics and line count
        input_prompt = {
            "input": f"اكتب قصيدة بعنوان '{poem_title}' من {num_lines} أشطار، على البحر {meter}، مع تضمين التشكيل.",
        }
        return input_prompt

    @staticmethod
    def display_response(response):
        # Display the structured response in a readable format
        print("\n--- Structured Response ---")
        print(response)

    @staticmethod
    def save_response_to_json_file(response):
        os.makedirs("ALLaM_output", exist_ok=True)

        # Save JSON data to a timestamped file
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_path = f"ALLaM_output/response_Tuned_Model_{timestamp}.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(response, json_file, ensure_ascii=False, indent=4)

        print(f"\nResponse saved to {file_path}")

    @staticmethod
    def transfer_response_to_json_file(response):
        if response:
            return json.dumps(response, ensure_ascii=False, indent=4)

    @staticmethod
    def extract_response(data):
        generated_text = data['results'][0]['generated_text']
        return generated_text

    def get_response(self, poem_title, num_lines, meter):
        # Send a request to the model with the constructed prompt
        access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5WZTRrVnZkc25JUUdrOWs0YzFRMlhrNjBmekhKSW1GUW5NWUJjN3A4ZkkifQ.eyJ1aWQiOiIxMDAwMzMxMDc2IiwidXNlcm5hbWUiOiJmYjlhNGZhZS0yNWM0LTRlNTEtOGM5Mi0zMzA4MTIzMjM1ZWYiLCJyb2xlIjoiVXNlciIsInBlcm1pc3Npb25zIjpbInNpZ25faW5fb25seSJdLCJncm91cHMiOlsxMDAzNiwxMDAwMF0sInN1YiI6ImZiOWE0ZmFlLTI1YzQtNGU1MS04YzkyLTMzMDgxMjMyMzVlZiIsImlzcyI6IktOT1hTU08iLCJhdWQiOiJEU1giLCJhcGlfcmVxdWVzdCI6dHJ1ZSwiaWF0IjoxNzMxMDU1NzMwLCJleHAiOjUzMzEwNTIxMzB9.B4q8H09URNCHUqGCyW5017nT_NhkkZbVcYpP8ewjphX_3bWsdaBrrbXBF_hC3cAogrzwa_rGao_Ybj4n6Cu4_KWvbRHKuUYBrgdR4pvmqSM6rVKS1qIEya5WwOPCS52x0aKXf2wnbyGaPbemULWRMfXsP7-hJOk4XOrwlHNl5pORRSEe1Rdt0ogIuLWAOZvZHh6dYwabNQLfhd0a3U4yVzWVJCo5W1rx4QhWTFZKbqIWaHDACpGC2ukGPIcOldGG0CLkvvBwkGgKOj2P1Mr7LiAnDNRcA9G9Az6Pbfo2-IRNUn2HocXcioLpnlwC96_JsdjiKI4DCLo8CjH_ToGcQg"

        # Step 2: Define the generation request
        url = "https://ai.deem.sa/ml/v1/deployments/4bfadd84-0409-4cfb-8542-832ceff24d92/text/generation?version=2023-05-29"

        input_prompt = self.construct_prompt(poem_title, num_lines, meter)

        body = {
            "input": f"<s> [INST] {input_prompt} [/INST]",
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 900,
                "repetition_penalty": 1
            },
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        return self.extract_response(response.json())
