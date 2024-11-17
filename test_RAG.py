from ALLaM_Manager import Manager
from ALLaM_RAG import RAG

# Initialize TokenManager and get the token
token_manager = Manager()
access_token = token_manager.get_access_token()

# Define a question
question = "ما هو الشعر العربي؟"

# Initialize ALLaMQueryHandler
rag = RAG(access_token, question)

# Use the handler to answer the question
response = rag.get_response(question)

rag.display_response(response)

# rag.save_response_to_json_file(response)
