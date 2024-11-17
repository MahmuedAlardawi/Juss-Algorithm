import requests

def format_and_display_response(data):
    # Extracting and formatting output
    generated_text = data['results'][0]['generated_text']
    generated_token_count = data['results'][0]['generated_token_count']
    input_token_count = data['results'][0]['input_token_count']
    stop_reason = data['results'][0]['stop_reason']
    model_id = data['model_id']
    created_at = data['created_at']
    warnings = data.get('system', {}).get('warnings', [])

    # Display structured output
    print("\n--- Generated Response ---")
    print(generated_text)

    print("\n--- Token Information ---")
    print(f"Generated Tokens: {generated_token_count}")
    print(f"Input Tokens: {input_token_count}")
    print(f"Stop Reason: {stop_reason}")

    print("\n--- System Information ---")
    print(f"Model ID: {model_id}")
    print(f"Created At: {created_at}")

    if warnings:
        print("\n--- Warnings ---")
        for warning in warnings:
            print(f"{warning['message']}\nMore info: {warning['more_info']}")

# Example usage
def get_and_display_response(input_data):
    # Step 1: Obtain the access token using your API key
    iam_url = "https://iam.cloud.ibm.com/identity/token"
    api_key = ""  # Replace with your IBM Cloud API key

    auth_response = requests.post(
        iam_url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=f"apikey={api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    )

    if auth_response.status_code != 200:
        raise Exception("Failed to obtain access token: " + auth_response.text)

    access_token = auth_response.json().get("access_token")

    # Step 2: Define the generation request
    url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

    body = {
        "input": f"<s> [INST] {input_data} [/INST]",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "repetition_penalty": 1
        },
        "model_id": "sdaia/allam-1-13b-instruct",
        "project_id": "15a67df8-d1d1-43b1-a44a-fa7265516cef"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    # Step 3: Send the request
    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    # Step 4: Call the formatting function to display the response
    format_and_display_response(response.json())

input_data1 = """
ما اسمك؟
"""
# Run the function to get and display the response
get_and_display_response(input_data1)
