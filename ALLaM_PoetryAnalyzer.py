import requests
import json
import os
from datetime import datetime

class PoemAnalyzer:
    def __init__(self, access_token):
        self.access_token = access_token

    @staticmethod
    def construct_prompt(poem, topic):
        # Define system prompt for poem analysis
        system_prompt = f"""
        أنت مساعد متخصص في شرح وتحليل القصائد العربية. عندما يُطلب منك الرد، يجب أن تقدم الإجابة وفقًا للتنسيق التالي:
        1. **القصيدة**: {{ضع هنا نص القصيدة واكتبها شطر في كل سطر}}
        2. **الموضوع**: {{حدد الموضوع الرئيسي الذي تناقشه القصيدة}}
        3. **الشرح العام**: {{قدّم شرحًا مبسطًا يوضح معاني القصيدة والمشاعر التي تعبر عنها}}
        4. **الشرح التفصيلي**: {{قدم تحليلاً مفصلاً لكل بيت من القصيدة، بما يشمل الأفكار الرئيسية والأدوات الأدبية المستخدمة}}
        5. **القصة**: {{قم بإنشاء قصة واقعية تمثل الشرح وتلتقط مشاعر وموضوعات القصيدة، بدون الإشارة إلى أنها مبنية على القصيدة. يجب أن تنتهي القصة بدون أي تعليق إضافي بعد نهايتها}}
        6. **أوصاف الصور**: {{قم بإنشاء عشرة أوصاف تفصيلية تُستخدم كمدخلات لتوليد صور على MidJourney. كل وصف يجب أن يعكس مشاعر وموضوعات القصيدة، ويشمل عناصر مرئية مثل الألوان، الإضاءة، الرموز، والمشاهد، لخلق صور تعبيرية مستوحاة من القصيدة}}
        

        ### مثال:
        
        1. العنوان الأول: القصيدة
        ريم على القاع بين البان والعلم
        أحل سفك دمي في الأشهر الحرم
        قالوا غزوت ورسل الله ما بعثوا
        لقتل نفس ولا جاؤوا لسفك دم
        
        2. العنوان الثاني: الموضوع
        تتناول القصيدة موضوع مدح النبي محمد صلى الله عليه وسلم والدفاع عن الإسلام والتصدي للشبهات والتهم الموجهة إليه.
        
        3. العنوان الثالث: الشرح العام
        تصف القصيدة جمال الطبيعة والهدوء الذي يحيط بها، لكن الشاعر يعبر عن الظلم الذي تعرض له بسبب اتهامه بالغزو والقتل. يؤكد الشاعر أن الإسلام دين سلام وأن رسل الله لم يبعثوا لقتل النفوس وسفك الدماء.
        
        4. العنوان الرابع: الشرح التفصيلي
        
        الشطر الأول: ريم على القاع بين البان والعلم
        الشرح: يصف الشاعر جمال الطبيعة والهدوء الذي يحيط به، مستخدماً صورة الريم (الغزال) الذي يعيش بين أشجار البان والعلم.
        
        الشطر الثاني: أحل سفك دمي في الأشهر الحرم
        الشرح: يعبر الشاعر عن الظلم الذي تعرض له بسبب اتهامه بالغزو والقتل، مشيراً إلى أن هذا الاتهام وقع في الأشهر الحرم التي تعتبر مقدسة ومحمية في الإسلام.
        
        الشطر الثالث: قالوا غزوت ورسل الله ما بعثوا
        الشرح: يؤكد الشاعر أن الإسلام دين سلام وأن رسل الله لم يبعثوا لقتل النفوس وسفك الدماء. يحاول الشاعر الدفاع عن الإسلام وتصحيح المفاهيم الخاطئة حوله.
        
        الشطر الرابع: لقتل نفس ولا جاؤوا لسفك دم
        الشرح: يؤكد الشاعر أن الإسلام دين سلام وأن رسل الله لم يبعثوا لقتل النفوس وسفك الدماء. يحاول الشاعر الدفاع عن الإسلام وتصحيح المفاهيم الخاطئة حوله.
        
        5. العنوان الخامس: القصة
        في قرية صغيرة وهادئة، عاش شاب يدعى أحمد. كان أحمد مسلمًا متدينًا ومحبًا للسلام. كان يقضي وقته بين دراسة القرآن والعمل في حقله. في يوم من الأيام، انتشرت شائعات حول أحمد بأنه شارك في معارك وغزوات.
        أثرت هذه الشائعات على سمعة أحمد وعلاقته بأصدقائه وجيرانه. قرر أحمد أن يدافع عن نفسه ويوضح الحقيقة للناس. جمع أحمد أصدقاءه وأقاربه وألقى خطابًا مؤثرًا يشرح فيه مبادئ الإسلام وأهمية السلام والمحبة.
        بعد سماعهم لخطاب أحمد، اقتنع الناس ببراءته وأدركوا أن الإسلام دين سلام ومحبة. اعتذروا لأحمد عن سوء الفهم وعادوا للتعامل معه بود واحترام.
        
        6. العنوان السادس: أوصاف الصور
        
        1. صورة لغزال هادئ بين أشجار البان والعلم: تظهر هذه الصورة جمال الطبيعة والهدوء الذي يحيط بالشاعر، وتكون بداية للتعبير عن السكينة التي يتمناها.
        2. صورة لنهر يجري بين التلال الخضراء والأشجار الكثيفة: تمثل الطبيعة التي تحيط بالشاعر وتعكس السلام الذي يسعى إليه.
        3. صورة لسماء ملبدة بالغيوم مع شعاع ضوء يخترقها: تعبر عن الأمل وسط الصعاب، وتشير إلى صمود الشاعر أمام الظلم.
        4. صورة لدموع تنهمر من عيني الشاعر: تجسد الألم والحزن الناتج عن اتهامه ظلماً.
        5. صورة لأحمد وهو يلقي خطابًا: تظهر لحظة الدفاع عن نفسه وشرح مبادئ الإسلام في مواجهة الاتهامات.
        6. صورة لأشخاص يستمعون بانتباه لخطاب أحمد: تمثل التأثير الإيجابي للخطاب، حيث ينصت الناس ويقتنعون ببراءته.
        7. صورة لأشخاص يتناقشون في حلقة حول معاني السلام والتفاهم: تعكس جو الحوار والتوضيح الذي يعزز الفهم المشترك.
        8. صورة لأحمد والناس يتعانقون تعبيرًا عن التصالح والتسامح: تعبر عن انتهاء النزاع وعودة السلام بين أحمد وأهل القرية.
        9. صورة لكتاب مفتوح بجوار نافذة تطل على منظر طبيعي: رمز للتعلم والتفكر في حقائق الدين ومعانيه.
        10. صورة لسماء ليلية تظهر النجوم: ترمز للهدوء الداخلي الذي يسعى إليه الشاعر بعد تجاوز التحديات، وتكون النهاية التي تمثل السلام الداخلي.

        """

        # Define few-shot examples
        few_shot_prompt = """
        القصيدة: أَكَادُ أَشُكُّ في نَفْسِي لأَنِّي أَكَادُ أَشُكُّ فيكَ وأَنْتَ مِنِّي يَقُولُ النَّاسُ إنَّكَ خِنْتَ عَهْدِي وَلَمْ تَحْفَظْ هَوَايَ وَلَمْ تَصُنِّي
        الموضوع: الحب والفراق
        الشرح: لقد أصبحت الشكوك وعدم اليقين من نفسي تراودني دائمًا، وهذا لأنني أوشكت أن أشكَّ بك يا حبيبي وأنت جزء منِي. ولذلك، إذا راودتني الشكوك حولك، فإنني أشك في نفسي، وقد صار الناس يتبادلون الأحاديث حول خيانتك لي، ويقولون: لقد خان العهد الذي قطعه معها ولم يحفظ الهوى الذي نما بينهما ولم يحفظها ولم يحافظ عليها.


        القصيدة: وَأنْتَ مُنَايَ أَجْمَعُهَا مَشَتْ بِي إِلَيْكَ خُطَى الشَّبَابِ المُطْمَئِنِّ وَقَدْ كَادَ الشَّبَابُ لِغَيْرِ عَوْدٍ يُوَلِّي عَنْ فَتَىً في غَيْرِ أَمْنِ
        الموضوع: الشباب والحب
        الشرح: وأنت أيها الحبيب كل المنى في حياتي والمراد والغاية. وقد سارت بي أيام الشباب إليك بكل ثقة واطمئنان. لكن الشباب أوشك أن يفارق هذا الفتى الذي يتقلب كثيرًا ولا يثبت على حب.


        القصيدة: وَهَا أَنَا فَاتَنِي القَدَرُ المُوَالِي بِأَحْلاَمِ الشَّبَابِ وَلَمْ يَفُتْنِي كَأَنَّ صِبَايَ قَدْ رُدَّتْ رُؤاهُ عَلَى جَفْنِي المُسَهَّدِ أَوْ كَأَنِّي
        الموضوع: الشباب والأحلام
        الشرح: رغم ما فاتني من أحلام الشباب، أشعر أنني ما زلت في ريعان شبابي. كأن الصبا الذي ولَّى قد عاد بأحلامه، وأسهر معه ليالي طويلة.


        القصيدة: يُكَذِّبُ فِيكَ كُلَّ النَّاسِ قَلْبِي وَتَسْمَعُ فِيكَ كُلَّ النَّاسِ أُذْنِي وَكَمْ طَافَتْ عَلَيَّ ظِلاَلُ شَكٍّ أَقَضَّتْ مَضْجَعِي وَاسْتَعْبَدَتْنِي
        الموضوع: الشك والعذاب
        الشرح: قلبي لا يصدق ما يقوله الناس عنك، حتى وإن سمعت أذني ذلك. لقد ساورتني الشكوك وحرمتني من النوم واستعبدتني بألمها.


        القصيدة: كَأَنِّي طَافَ بِي رَكْبُ اللَيَالِي يُحَدِّثُ عَنْكَ فِي الدُّنْيَا وَعَنِّي عَلَى أَنِّي أُغَالِطُ فِيكَ سَمْعِي وَتُبْصِرُ فِيكَ غَيْرَ الشَّكِّ عَيْنِي
        الموضوع: الثقة والشك
        الشرح: أشعر وكأن الليالي تتحدث عني وعن الحب الذي كان بيننا. لكن رغم كل ما أسمع، فإنني أرفض الشك وأثق بك كما أثق بنفسي.
        
        """

        # Combine system prompt, few-shot examples, and user query
        input_prompt = f"<s> [INST] {system_prompt}\n\n{few_shot_prompt}\n\nقصيدة: {poem}\nموضوع: {topic} [/INST]"
        return input_prompt

    @staticmethod
    def display_response(response):
        # Display the structured response in a readable format
        print("\n--- Structured Response ---")
        for key, value in response['structured_response'].items():
            print(f"{key}:")
            for v in value:
                print(v)
            print()

    @staticmethod
    def save_response_to_json_file(response):
        os.makedirs("ALLaM_output", exist_ok=True)

        # Save JSON data to a timestamped file
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_path = f"ALLaM_output/response_PoemAnalysis_{timestamp}.json"

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

        content_keys = [
            "القصيدة", "الموضوع", "الشرح العام",
            "الشرح التفصيلي", "القصة", "أوصاف الصور"
        ]

        line_idx = 0
        current_key = 0

        generated_text = data['results'][0]['generated_text']

        # Parse generated text to extract each component based on labeled titles
        lines = generated_text.split("\n")

        content_keys = [
            "القصيدة", "الموضوع", "الشرح العام",
            "الشرح التفصيلي", "القصة", "أوصاف الصور"
        ]

        # Initialize variables
        line_idx = 0
        current_key = 0
        structured_response = {}

        # Parsing loop
        while line_idx < len(lines) and current_key < len(content_keys):
            line = lines[line_idx].strip()

            # Check if the line contains the current title we are looking for
            if content_keys[current_key] in line:
                # Initialize the response content for the current key
                structured_response[content_keys[current_key]] = []

                lll = lines[line_idx].split(": ")
                if len(lll) > 1:
                    structured_response[content_keys[current_key]].append(lll[-1])

                # Move to the next line and collect content for the current key
                line_idx += 1
                while line_idx < len(lines) and (
                        current_key == len(content_keys) - 1 or content_keys[current_key + 1] not in lines[line_idx]
                ):
                    # Append the line to the current key's content
                    structured_response[content_keys[current_key]].append(lines[line_idx].strip())
                    line_idx += 1

                # Move to the next key
                current_key += 1

            else:
                line_idx += 1  # Move to the next line if no match is found

        for key in structured_response:
            # Remove elements that are empty strings or evaluate to False (like None)
            structured_response[key] = [elem for elem in structured_response[key] if elem]

        # Combine structured response with the full response data
        combined_data = {
            "structured_response": structured_response,
            "full_response": data
        }

        return combined_data

    def get_response(self, poem, topic):
        # Send a request to the model with the constructed prompt
        url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        input_prompt = self.construct_prompt(poem, topic)

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
