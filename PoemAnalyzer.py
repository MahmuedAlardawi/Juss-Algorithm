import re
from datetime import datetime
import json
import os

from PoemTokenizer import PoemTokenizer
from PoeticUnits import PoeticUnits

class PoemAnalyzer:
    def __init__(self, poem):
        self.poem = poem.strip()
        self.result = self.define_result()

    def analyze(self):

        final_result = None
        poem_tokenizer = PoemTokenizer(self.poem).tokenized_poem

        best_match = 0
        for key, value in poem_tokenizer.items():
            poetic_units = PoeticUnits(value)

            comparison = poetic_units.compare(poetic_units.taweel_see())
            results = poetic_units.result(comparison)
            result = poetic_units.get_match(results)

            if best_match < result[1]:
                best_match = result[1]
                final_result = [key, value, result[0], best_match]

        return final_result

    @staticmethod
    def describe(result):
        description = {}

        poem = result[0]
        tokenized_poem = result[1]
        meter = result[2]
        percentage = result[3]

        description['الكتاب العروضية'] = poem
        description['الكتابة الرقمية'] = tokenized_poem
        description['البحر'] =' '.join(tafeela[1] for tafeela in meter)
        description['نسبة التطابق'] = f'{percentage:.2f}%'

        poem_no_space = ''.join(poem.split())

        index = 0
        for i in range(len(meter)):
            tokenized_tafeela = meter[i][0]
            tafeela = meter[i][1]

            change = {
                'قبض': 'القبض: هو حذف الحرف الساكن الخامس من التفعيلة في البيت الشعري للحفاظ على الوزن',
                'حذف': 'الحذف: هو حذف الحرف المتحرك من آخر التفعيلة لتعديل وزن البيت الشعري',
                None: None,
            }

            change = change[meter[i][2]]
            orginal_tafeela = meter[i][3]

            word = poem_no_space[index * 2 : index * 2  + len(tokenized_tafeela)*2]
            tokenized_word = ''
            for diacritic in word:
                if re.match(r'[َُِ]', diacritic):
                    tokenized_word += '1'
                elif re.match(r'ْ', diacritic):
                    tokenized_word += '0'

            comp = ''
            if len(tokenized_word) < len(tokenized_tafeela):
                l = len(tokenized_tafeela) - len(tokenized_word)
                for i in range(l):
                    tokenized_word += '#'

            for j in range(len(tokenized_word)):
                if tokenized_word[j] == tokenized_tafeela[j]:
                    comp += tokenized_word[j]  # Keep the matching element
                else:
                    comp += '#'  # Replace mismatch with '#'

            c = comp


            counter = 0
            for j in comp:
                if j != '#':
                    counter += 1

            word_percentage = counter/len(tokenized_tafeela) * 100

            index += len(tokenized_tafeela)

            description[i] = {'الكلمة': word,
                                'رمز الكلمة': tokenized_word,
                                'التفعيلة': tafeela,
                                'الرمز التفعيلة': tokenized_tafeela,
                                'c': comp,
                                'نسبة المطابقة': f'{word_percentage:.2f}%',
                                'الزحاف والعلة': change,
                                'التفعيلة الأساسية': orginal_tafeela
                                }

        return description

    def define_result(self):
        result = self.analyze()

        describe = self.describe(result)

        return describe

    @staticmethod
    def display_result(result):
        # Display only the generated text for readability
        print("\n--- Structured Response ---")
        for key, value in result.items():
            print(f"{key}: {value}")

    @staticmethod
    def save_result_to_json_file(result):
        os.makedirs("ALLaM_output", exist_ok=True)

        # Save JSON data to a timestamped file
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_path = f"Analysis_output/result_{timestamp}.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(result, json_file, ensure_ascii=False, indent=4)

        print(f"\nResponse saved to {file_path}")

    @staticmethod
    def transfer_result_to_json_file(result):
        if result:
            return json.dumps(result, ensure_ascii=False, indent=4)
