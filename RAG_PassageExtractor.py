import json
import os
from datetime import datetime


class PassageExtractor:
    def __init__(self):
        pass

    @staticmethod
    def load_json_data(filepath):
        if not os.path.exists(filepath):
            print(f"Error: File not found - {filepath}")
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def display_passages(passages):
        # Display only the generated text for readability
        print("\n--- Passages ---")
        for passage in passages:
            for k, v in passage.items():
                print(k, ":")
                print(v)
            print()

    @staticmethod
    def save_passages_to_json_file(passages):
        os.makedirs("ALLaM_output", exist_ok=True)

        # Save JSON data to a timestamped file
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_path = f"Book_output/retrieved_passages_{timestamp}.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(passages, json_file, ensure_ascii=False, indent=4)

        print(f"\nResponse saved to {file_path}")

    @staticmethod
    def transfer_passages_to_json_file(passages):
        if passages:
            return json.dumps(passages, ensure_ascii=False, indent=4)

    def extract_passages(self, data, limit=5):
        file = self.load_json_data("RAG_data/book_pages.json")
        if not file:
            print("Error: Unable to load book pages data.")
            return []

        passages = []
        # Limit to the first 5 titles if data has more
        titles_to_search = data[:limit]

        for page in file.get("محتوى الكتاب", []):
            for title in titles_to_search:
                if title == page.get("title"):
                    passages.append({
                        "title": title,
                        "page_content": page.get("content")
                    })

        return passages

    def extract_passages_sea_type(self, sea_type):
        file = self.load_json_data("RAG_data/book_pages.json")
        if not file:
            print("Error: Unable to load book pages data.")
            return []

        passages = []

        for page in file.get("محتوى الكتاب", []):
            if sea_type in page.get("title"):
                passages.append({
                    "title": page.get("title"),
                    "page_number": page.get("page_number"),
                    "page_content": page.get("content")
                })

        return passages
