import json
from datetime import datetime

import chromadb
import os
import shutil
from langchain_huggingface import HuggingFaceEmbeddings


class DBManager:
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.emb_func = HuggingFaceEmbeddings(model_name=model_name)

    @staticmethod
    def load_json_data(filepath):
        if not os.path.exists(filepath):
            print(f"Error: File not found - {filepath}")
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def create_documents(book_content):
        # Extract documents
        documents = [{
            "title": page['title'],
            "content": page['content'],
            "page_number": page["page_number"],
            "url": page["url"],
            "footnotes": page["footnotes"]
        } for page in book_content]

        return documents

    def embed_documents(self, text_list):
        return self.emb_func.embed_documents(text_list)

    @staticmethod
    def initialize_db(db_path, collection_name):
        # Clears any existing data and initializes a new database
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
        client = chromadb.PersistentClient(path=db_path)
        return client.get_or_create_collection(name=collection_name)

    @staticmethod
    def load_db(db_path, collection_name):
        # Loads an existing database without deleting data, or raises an error if not found
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database path '{db_path}' does not exist.")
        client = chromadb.PersistentClient(path=db_path)
        return client.get_collection(name=collection_name)

    @staticmethod
    def flatten_footnotes(footnotes):
        if isinstance(footnotes, list) and footnotes:
            return "; ".join([f"{note['number']}: {note['text']}" for note in footnotes])
        return ""

    def add_documents_to_db(self, collection, documents, embeddings):
        for idx, doc in enumerate(documents):
            footnotes_str = self.flatten_footnotes(doc["footnotes"])

            collection.add(
                ids=[str(idx)],
                documents=[doc["content"]],
                metadatas=[{
                    "title": doc["title"],
                    "page_number": doc["page_number"],
                    "url": doc["url"],
                    "footnotes": footnotes_str,
                }],
                embeddings=[embeddings[idx]]
            )

    def create_db(self, embedding_type='content'):
        # Load data
        filepath = 'RAG_data/book_pages.json'
        data = self.load_json_data(filepath)
        book_content = data["محتوى الكتاب"]

        # Extract documents
        documents = self.create_documents(book_content)

        # Generate embeddings for content and titles
        embeddings = self.embed_documents([doc[embedding_type] for doc in documents])

        # Initialize databases
        db = self.initialize_db(f"db_{embedding_type}", f"{embedding_type}_collection")

        # Add documents to the content database
        self.add_documents_to_db(db, documents, embeddings)

        print(f"Number of documents in the db collection: {db.count()}")

    def query_db(self, db_collection, query_text, n_results=5):
        # Embed the query text
        query_embedding = self.emb_func.embed_documents([query_text])

        # Perform the query on the specified database
        results = db_collection.query(
            query_embeddings=query_embedding,  # Use the query embedding
            n_results=n_results  # Number of results to retrieve
        )

        documents = results['documents']  # The content of the documents
        metadatas = results['metadatas']  # The associated metadata

        combined_results = []
        for doc, meta in zip(documents[0], metadatas[0]):
            combined_results.append({
                "document": doc,
                "metadata": meta
            })

        # Rerank based on page number or any other metadata field
        combined_results.sort(key=lambda x: int(x['metadata']['page_number']))  # Sorting by page number

        # Format the results for readability
        formatted_results = []
        for result in combined_results:
            formatted_results.append({
                "title": result["metadata"]["title"],
                "content": result["document"],
                "page_number": result["metadata"]["page_number"],
                "url": result["metadata"]["url"],
                "footnotes": result["metadata"]["footnotes"],
            })

        return formatted_results

    @staticmethod
    def display_passages(query):
        # Display only the generated text for readability
        print("\n--- Query ---")
        for passage in query:
            for k, v in passage.items():
                print(k, ":")
                print(v)
            print()

    @staticmethod
    def save_query_to_json_file(query):
        os.makedirs("ALLaM_output", exist_ok=True)

        # Save JSON data to a timestamped file
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_path = f"Book_output/retrieved_query_{timestamp}.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(query, json_file, ensure_ascii=False, indent=4)

        print(f"\nResponse saved to {file_path}")

    @staticmethod
    def transfer_query_to_json_file(query):
        if query:
            return json.dumps(query, ensure_ascii=False, indent=4)
