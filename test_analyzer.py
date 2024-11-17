from sympy.physics.units import percent

from PoemAnalyzer import PoemAnalyzer
import json
import pandas as pd

minimized_file_path = 'ALLaM_fineTuned_output/generated_poems.json'

with open(minimized_file_path, 'r', encoding='utf-8') as file:
    generated_poems = json.load(file)

verse_list = []
for poem in generated_poems:
    poem_list = poem.strip().split('\n')
    for i in range(len(poem_list)):
        if i != 0:
            if poem_list[i] not in verse_list:
                verse_list.append(poem_list[i])


verse_list_1 = []
for i in range(len(verse_list)):
    if len(verse_list[i]) < 10:
        continue
    else:
        verse_list_1.append(verse_list[i])

results = []
for verse in verse_list:
    try:
        analyzer = PoemAnalyzer(verse)
        result = analyzer.result
        results.append(result)
    except Exception as e:
        print(f"An error occurred: {e}")
        continue

percentage_list = []
for result in results:
    if int(result['نسبة التطابق'].split('.')[0]) >= 70:
        percentage_list.append(result['نسبة التطابق'])

total = 0
for percentage in percentage_list:
    num = float(percentage.split('%')[0])
    total += num

accuracy = total/len(percentage_list)
print(f'inputs: {len(percentage_list)}')
print(f'accuracy: {accuracy}%')