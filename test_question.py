from ALLaM_Manager import Manager
from ALLaM_QuestionFormatter import QuestionFormatter
from RAG_PassageExtractor import PassageExtractor

# Initialize TokenManager and get the token
token_manager = Manager()
access_token = token_manager.get_access_token()

# Initialize QuestionFormatter with the access token
question_formatter = QuestionFormatter(access_token)

# Define the question and get the response
question = "ما عدد البحور الشعرية؟"
response = question_formatter.get_response(question)


# Display and save the structured response
question_formatter.display_response(response)
# question_formatter.save_response_to_json_file(response)

# Passage extractor
passage_extractor = PassageExtractor()
retrieved_data = passage_extractor.extract_passages(
    response['structured_response']['عناوين ذات الصلة'])

passage_extractor.display_passages(retrieved_data)
# passage_extractor.save_passages_to_json_file(retrieved_data)
