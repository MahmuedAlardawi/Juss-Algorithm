import requests
import json
import os
from datetime import datetime

class QuestionFormatter:
    def __init__(self, access_token):
        self.access_token = access_token

    @staticmethod
    def construct_prompt(question):
        # Define the system prompt
        system_prompt = f"""
        أنت مساعد متخصص في إعادة صياغة الأسئلة المتعلقة بالشعر، مما يسهل استخدامها في أنظمة استرجاع المعلومات. عندما يُطلب منك إعادة صياغة سؤال حول موضوع معين في الشعر أو علم العروض، يجب أن تقدم الإصلاحات وفقًا للتنسيق التالي:
        1. **السؤال**: {question}
        2. **إعادة الصياغة المبسطة**: {{قدم إعادة صياغة بسيطة للسؤال بحيث يكون مفهومًا بشكل مباشر}}
        3. **صياغة بديلة**: {{قدم صيغة مختلفة تمامًا للسؤال، مع الحفاظ على نفس المعنى}}
        4. **تلخيص السؤال**: {{اختصر السؤال إلى الفكرة الأساسية المرتبطة بالموضوع}}
        5. **التفصيل**: {{قم بتوسيع السؤال ليشمل جميع التفاصيل المحتملة المتعلقة بالموضوع، بما يشمل السياق والأسلوب}}
        6. **استخراج مصطلح رئيسي للتصفية**: {{حدد مصطلحاً واحداً رئيسياً يمكن استخدامه كعامل تصفية أساسي في البحث داخل قاعدة البيانات، بحيث يعبر عن الفكرة الأساسية للسؤال أو الموضوع الرئيسي}}
        7. **استخراج الكلمات المفتاحية**: {{حدد الكلمات المفتاحية الرئيسية المتعلقة بالموضوع من السؤال}}
        8. **عناوين ذات الصلة**: {{استعرض قائمة العناوين المتوفرة في الكتاب، وحدد العناوين التي قد تحتوي على إجابات أو معلومات مرتبطة بالسؤال، مع مراعاة اختيار العناوين التمهيدية أو العامة إن كانت مناسبة للسؤال}}
        

        ### قائمة العناوين المتوفرة في الكتاب:

        - مقدمة
        - تمهيد
        - أوزان البحور
        - البحر الطويل
        - تدريبات على البحر الطويل
        - البحر المديد
        - تدريبات على بحر المديد
        - البحر البسيط
        - تدريبات على بحر البسيط
        - البحر الوافر
        - تدريبات على بحر الوافر
        - البحر الكامل
        - تدريبات على بحر الكامل
        - البحر الهزج
        - تدريبات على بحر الهزج
        - البحر الرجز
        - تمرينات على بحر الرجز
        - البحر الرمل
        - تدريبات على بحر الرمل
        - البحر السريع
        - تدريبات على بحر السريع
        - البحر المنسرح
        - تدريبات على بحر المنسرح
        - البحر الخفيف
        - تدريبات على بحر الخفيف
        - البحر المضارع
        - تمرينات على بحر المضارع
        - البحر المقتضب
        - تدريبات على بحر المقتضب
        - البحر المجتث
        - تدريبات على بحر المجتث
        - البحر المتقارب
        - تدريبات على بحر المتقارب
        - البحر المتدارك
        - مفاتيح البحور
        - القافية
        - حروف القافية
        - الزحافات والعلل
        - أقسام العلة
        - العلل الجارية مجرى الزحاف
        - دوائر العروض
        - تدريبات

        ### مثال:

        السؤال: ما هو البحر في علم العروض؟

        1. العنوان الأول: السؤال: ما هو البحر في علم العروض؟
        2. العنوان الثاني: إعادة الصياغة المبسطة: ما هو البحر في علم العروض؟
        3. العنوان الثالث: صياغة بديلة: ما هو الوزن الشعري الذي يُعرف بالبحر في دراسة الشعر العربي؟
        4. العنوان الرابع: تلخيص السؤال: البحر في علم العروض.
        5. العنوان الخامس: التفصيل: البحر في علم العروض هو مصطلح يُطلق على مجموعة من الأبيات الشعرية التي تتشابه في الوزن الشعري وتتبع نفس النمط الإيقاعي. يُعتبر البحر وحدة أساسية لتنظيم الشعر وتحديد إيقاع القصيدة.
        6. العنوان السادس: استخراج مصطلح رئيسي للتصفية: البحر.
        7. العنوان السابع: استخراج الكلمات المفتاحية: البحر، علم العروض، الأبيات الشعرية، الوزن الشعري، النمط الإيقاعي.
        8. العنوان الثامن: عناوين ذات الصلة: مقدمة، تمهيد، أوزان البحور.
        """

        # Return prompt ready to send
        return f"<s> [INST] {system_prompt}\n\nالسؤال: {question} [/INST]"

    @staticmethod
    def display_response(response):
        # Display only the generated text for readability
        print("\n--- Structured Response ---")
        for key, value in response['structured_response'].items():
            print(f"{key}: {value}")

    @staticmethod
    def save_response_to_json_file(response):
        os.makedirs("ALLaM_output", exist_ok=True)

        # Save JSON data to a timestamped file
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_path = f"ALLaM_output/response_ReformatQuestion_{timestamp}.json"
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

        # Parse generated text to extract each component based on labeled titles
        lines = generated_text.split("\n")
        structured_response = {}

        for line in lines:
            if "العنوان الأول:" in line:
                structured_response["السؤال"] = line.split(": ")[-1].strip()
            elif "العنوان الثاني:" in line:
                structured_response["إعادة الصياغة المبسطة"] = line.split(": ")[-1].strip()
            elif "العنوان الثالث:" in line:
                structured_response["صياغة بديلة"] = line.split(": ")[-1].strip()
            elif "العنوان الرابع:" in line:
                structured_response["تلخيص السؤال"] = line.split(": ")[-1].strip()
            elif "العنوان الخامس:" in line:
                structured_response["التفصيل"] = line.split(": ")[-1].strip()
            elif "العنوان السادس:" in line:
                structured_response["استخراج مصطلح رئيسي للتصفية"] = line.split(": ")[-1].strip()
            elif "العنوان السابع:" in line:
                structured_response["استخراج الكلمات المفتاحية"] = [item.strip() for item in
                                                                    line.split(": ")[-1].replace(".", "").split("،")]
            elif "العنوان الثامن:" in line:
                structured_response["عناوين ذات الصلة"] = [item.strip() for item in
                                                           line.split(": ")[-1].replace(".", "").split("،")]

        # Combine structured response with the full response data
        combined_data = {
            "structured_response": structured_response,
            "full_response": data
        }

        return combined_data

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
