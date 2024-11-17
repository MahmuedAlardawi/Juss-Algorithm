import requests
import json
import os
from datetime import datetime

class Daicritizer:
    def __init__(self, access_token):
        self.access_token = access_token

    @staticmethod
    def construct_prompt(poem):
        # Define the system prompt with strict response structure
        system_prompt = f"""
        أنت مساعد متخصص في تشكيل النصوص العربية، ويُطلب منك إضافة الحركات المناسبة فقط على الحروف التي تفتقر للتشكيل في أبيات الشعر دون تغيير التشكيل الموجود مسبقاً. عند إضافة التشكيل، اتبع هذه التعليمات بدقة:

        1. **أضف التشكيل فقط على الحروف التي لا تحتوي على حركات**: ضع الحركات المناسبة للأحرف التي تفتقر للتشكيل حسب سياق البيت الشعري.
        2. **لا تغيّر الحروف أو الكلمات التي تحتوي بالفعل على حركات**: تجاهل تماماً الكلمات أو الحروف التي تحتوي على حركات مسبقاً، واعمل فقط على الأجزاء التي لا تحتوي على تشكيل.
        3. **احرص على الدقة في إضافة التشكيل بما يناسب الوزن الشعري**: يجب أن يكون التشكيل المضاف ملائماً لبنية الوزن الشعري وملائماً للمعنى.
        4. **ضع الحركات بعد الشدة عند إضافتها**: إذا كان الحرف يحتوي على شدة، فاحرص على وضع الحركة بعد الشدة مباشرةً لتكون متناسقة وصحيحة.

        ### أمثلة:

        النص الأصلي:
        إذا غامرت في شرف مروم فلا تقنع بما دون النجوم
        النص المشكّل:
        إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومٍ فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ

        النص الأصلي:
        من كان فوق محلّ الشمس رؤيته
        النص المشكّل:
        مَنْ كَانَ فَوْقَ مَحَلِّ الشَّمْسِ رُؤْيَتُهُ

        النص الأصلي:
        وقفت على بابك الشّرقي
        النص المشكّل:
        وَقَفْتُ عَلَى بَابِكَ الشَّرْقِيِّ

        **ملاحظة**: أجب فقط بالنص المشكّل بصيغة محددة كما يلي:

        النص المشكّل:
        وَقَفْتُ عَلَى بَابِكَ الشَّرْقِيِّ
        """

        # Return prompt ready to send with input poem
        return f"<s> [INST] {system_prompt}\n\nالنص: {poem} [/INST]"

    @staticmethod
    def display_response(response):
        # Display only the generated text for readability
        print("\n--- Response ---")
        print(response)

    @staticmethod
    def save_response_to_json_file(response):
        os.makedirs("ALLaM_output", exist_ok=True)

        # Save JSON data to a timestamped file
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_path = f"ALLaM_output/RAG_output_{timestamp}.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(response, json_file, ensure_ascii=False, indent=4)

        print(f"\nResponse saved to {file_path}")

    @staticmethod
    def transfer_response_to_json_file(response):
        if response:
            return json.dumps(response, ensure_ascii=False, indent=4)

    @staticmethod
    def extract_response(data):
        response = data['results'][0]['generated_text']
        response = response.split(':')
        return response[1]

    def get_response(self, question):
        url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        input_prompt = self.construct_prompt(question)

        body = {
            "input": input_prompt,
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
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        return self.extract_response(response.json())
