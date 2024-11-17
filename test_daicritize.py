from ALLaM_Manager import Manager
from ALLaM_Diacritizer import Daicritizer

# Initialize TokenManager and get the token
token_manager = Manager()
access_token = token_manager.get_access_token()

# Initialize QuestionFormatter with the access token
question_formatter = Daicritizer(access_token)

# Define the question and get the response
question = """
تزيدُ اشتعالًا كلما مرَّ الزمانُ

"""
response = question_formatter.get_response(question)

# Display and save the structured response
question_formatter.display_response(response)
# question_formatter.save_response_to_json_file(response)

