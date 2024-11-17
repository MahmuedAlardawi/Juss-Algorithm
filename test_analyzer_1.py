from ALLaM_Manager import Manager
from ALLaM_Diacritizer import Daicritizer
from PoemAnalyzer import PoemAnalyzer

# Initialize TokenManager and get the token
token_manager = Manager()
access_token = token_manager.get_access_token()

# Initialize QuestionFormatter with the access token
daicritizer = Daicritizer(access_token)

# Define the question and get the response
verse = """
وَيَسْعَى إِلَى كُلِّ فَوْزٍ وَمُشْتَهَى
"""
response = daicritizer.get_response(verse)
print(response)

# Define the question and get the response
# verse = response

analyzer = PoemAnalyzer(verse)
result = analyzer.result

# Display and save the structured response
analyzer.display_result(result)

