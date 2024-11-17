import random

import requests
import json
import os

from datetime import datetime

from ALLaM_QuestionFormatter import QuestionFormatter
from RAG_PassageExtractor import PassageExtractor
import pandas as pd


class RAG:
    def __init__(self, access_token=None, question=None):
        self.access_token = access_token
        self.question = question

    def query(self, question):
        # Initialize QuestionFormatter with the access token
        question_formatter = QuestionFormatter(self.access_token)

        response = question_formatter.get_response(question)

        # Passage extractor
        passage_extractor = PassageExtractor()
        return passage_extractor.extract_passages(
            response['structured_response']['عناوين ذات الصلة'])

    def construct_prompt(self, question, max_passages=10):
        query = self.query(self.question)

        # Randomly select up to max_passages from query_data
        selected_passages = random.sample(query, min(len(query), max_passages))

        # Build the system prompt with a clear role definition, introductory note, and instructions
        system_prompt = (
            "***لا تجب على الإسئلة الغير متعلقة في الشعر العربي وعلم العروض***\n\n"
            "تعليمات:\n"
            "- أنت معلم شعر وأدب متخصص في الإجابة على الأسئلة المتعلقة بالشعر العربي وتقديم شروحات مفصلة حولها.\n"
            "- دورك هو مساعدة الطلاب والمهتمين بالأدب الشعري على فهم القصائد وأوزانها ومعانيها بأسلوب واضح وسهل.\n"
            "- يجب أن تقتصر إجاباتك على موضوع الشعر العربي فقط. إذا كان السؤال لا يتعلق بالشعر أو الأدب الشعري، "
            "أجب فقط بعبارة: 'عذرًا، لا يمكنني الإجابة على الأسئلة غير المتعلقة بالشعر.'\n"
            "- قدم تفسيرات دقيقة ومبسطة تراعي مستوى فهم القارئ، وتجنب استخدام المصطلحات المعقدة دون شرحها.\n\n"
            "النصوص ذات الصلة:\n"
        )
        for passage in query[:10]:
            title = passage.get("title", "بدون عنوان")
            content = passage.get("page_content", "")
            system_prompt += f"\n- العنوان: {title}\nالمحتوى: {content}\n"

        # Combine with the question to form the final prompt
        return f"<s> [INST] {system_prompt}\n\nالسؤال: {question} [/INST]"

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
        return data['results'][0]['generated_text']

    def get_response(self, question):
        url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        input_prompt = self.construct_prompt(question)

        body = {
            "input": input_prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 2000,
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

    @staticmethod
    def questions_for_evaluation():
        return [
    "ما هو علم العروض؟",
    "من هو مؤسس علم العروض؟",
    "ما معنى التفعيلة في الشعر؟",
    "ما هي البحور الشعرية؟",
    "ما الفرق بين البحر الطويل والبحر الكامل؟",
    "ما المقصود بالزحاف في علم العروض؟",
    "ما هي تفعيلة البحر الوافر؟",
    "كيف يوزن البيت الشعري؟",
    "ما هو العروض في البيت الشعري؟",
    "لماذا يحتاج الشاعر إلى علم العروض؟",
    "ما هي تفعيلة البحر البسيط؟",
    "ما هي تفعيلة البحر المديد؟",
    "ما هي تفعيلة البحر الخفيف؟",
    "ما هي تفعيلة البحر السريع؟",
    "ما هي تفعيلة البحر المنسرح؟",
    "ما هي تفعيلة البحر الرجز؟",
    "ما هي تفعيلة البحر الرمل؟",
    "ما هي تفعيلة البحر الهزج؟",
    "ما هي تفعيلة البحر الكامل؟",
    "ما هي تفعيلة البحر المتقارب؟",
    "ما هي تفعيلة البحر المتدارك؟",
    "ما الفرق بين البحر المتقارب والبحر المتدارك؟",
    "ما هو الفرق بين العروض والضرب في البيت الشعري؟",
    "ما هي الزحافات والعلل في علم العروض؟",
    "كيف يساعد علم العروض على تحسين جودة الشعر؟",
    "ما معنى القافية في الشعر العربي؟",
    "ما هي وظيفة الكتابة العروضية؟",
    "كيف يمكن تحديد البحر الذي ينتمي إليه البيت الشعري؟",
    "ما هو البحر المضارع؟",
    "ما هو البحر المجتث؟"
]

    @staticmethod
    def query_for_evaluation(query):
        passages_list = []

        # Iterate through each passage and format it into a structured string
        for passage in query[:10]:
            title = passage.get("title", "بدون عنوان")
            page_content = passage.get("page_content", "غير متوفر")

            # Append each passage's content to the combined string
            combined_string = (
                f"العنوان: {title}\n"
                f"المحتوى: {page_content}\n\n"
            )

            passages_list.append(combined_string)

        return passages_list

    def generated_answer_for_evaluation(self, question):
        return self.get_response(question)

    @staticmethod
    def referenced_answer_for_evaluation():
        return [
    "علم العروض هو علم يدرس أوزان الشعر العربي ويحدد قواعدها.",
    "مؤسس علم العروض هو الخليل بن أحمد الفراهيدي.",
    "التفعيلة هي الوحدة الوزنية الأساسية التي يتكون منها البيت الشعري.",
    "البحور الشعرية هي الأوزان التي تُبنى عليها أبيات الشعر وعددها 16 بحرًا.",
    "البحر الطويل يتكون من تكرار 'فعولن مفاعيلن'، بينما البحر الكامل يتكون من 'متفاعلن'، ويختلفان في الإيقاع.",
    "الزحاف هو تغيير في التفعيلة بحذف أو تغيير حرف معين، ويعتبر جائزًا.",
    "تفعيلة البحر الوافر هي 'مفاعلتن'.",
    "يوزن البيت الشعري بتقسيمه إلى تفاعيل وفق البحر الذي ينتمي إليه.",
    "العروض هي التفعيلة الأخيرة من الشطر الأول في البيت الشعري.",
    "علم العروض ضروري للشاعر لضبط الأوزان وتجنب الأخطاء وزيادة جمال القصيدة.",
    "تفعيلة البحر البسيط هي 'مستفعلن فاعلن'.",
    "تفعيلة البحر المديد هي 'فاعلاتن فاعلن'.",
    "تفعيلة البحر الخفيف هي 'فاعلاتن مستفعلن'.",
    "تفعيلة البحر السريع هي 'مستفعلن مستفعلن'.",
    "تفعيلة البحر المنسرح هي 'مستفعلن مفعولات'.",
    "تفعيلة البحر الرجز هي 'مستفعلن'.",
    "تفعيلة البحر الرمل هي 'فاعلاتن'.",
    "تفعيلة البحر الهزج هي 'مفاعيلن'.",
    "تفعيلة البحر الكامل هي 'متفاعلن'.",
    "تفعيلة البحر المتقارب هي 'فعولن'.",
    "تفعيلة البحر المتدارك هي 'فاعلن'.",
    "البحر المتقارب يتكون من 'فعولن'، بينما البحر المتدارك يتكون من 'فاعلن'.",
    "العروض هي التفعيلة الأخيرة من الشطر الأول، والضرب هو التفعيلة الأخيرة من الشطر الثاني.",
    "الزحافات هي تغييرات جزئية في التفعيلات، والعلل تغييرات كلية تؤثر على التفعيلة.",
    "علم العروض يساعد الشاعر على ضبط وزن القصيدة مما يحسن من جودتها.",
    "القافية هي نهاية البيت الشعري وتتكون من حروف محددة.",
    "الكتابة العروضية تُظهر النطق الفعلي للمقاطع الصوتية في البيت الشعري.",
    "يمكن تحديد البحر الذي ينتمي إليه البيت بتقطيع البيت إلى تفاعيل.",
    "البحر المضارع يتكون من 'مفاعيلن فاعلاتن'.",
    "البحر المجتث يتكون من 'مستفعلن فاعلاتن'."
]

    def evaluation_data(self, question, reference):
        query = self.query(question)
        passages_list = self.query_for_evaluation(query)

        answer = self.generated_answer_for_evaluation(question)

        # Combine all components
        data = {
            "user_input": question,
            "retrieved_contexts": passages_list,
            "response": answer,
            "reference": reference,
            "rubric": None
        }

        return data

    @staticmethod
    def save_evaluation_data_to_json_file(df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame.")

        os.makedirs("ALLaM_output", exist_ok=True)

        # Save JSON data to a timestamped file
        file_path = f"ALLaM_evaluation_output/RAG_evaluation_data.json"

        # Convert DataFrame to JSON and save
        df.to_json(file_path, orient="records", force_ascii=False, indent=4)

        print(f"\nEvaluation saved to {file_path}")
