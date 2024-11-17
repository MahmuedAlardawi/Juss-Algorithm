from ALLaM_Manager import Manager
from ALLaM_PoetryAnalyzer import PoemAnalyzer

# Initialize TokenManager and get the token
token_manager = Manager()
access_token = token_manager.get_access_token()

# Initialize QuestionFormatter with the access token
poem_analyzer = PoemAnalyzer(access_token)

# Define the question and get the response
poem ="""
عَلَامُ أَتَى بِالمَزَايَا إِلَى العِلْمِ
ذَكَاءٌ يُضِيءُ الدُّرُوبَ لَنَا أَمَلًا
يُنَافِسُ فِي سَاحَةِ العِلْمِ جَاهِدًا  
وَيَبْنِي لَنَا فِي المَعَارِفِ مَنْزِلًا  
يَرَى فِي طَرِيقِ النُّجُومِ طُمُوحَهُ
وَيَسْعَى إِلَى كُلِّ فَوْزٍ وَمُشْتَهَى

"""
topic = "نموذج علام في الذكاء الإصطناعي"
response = poem_analyzer.get_response(poem, topic)


# Display the structured response
poem_analyzer.display_response(response)

# Optionally, save the full response to a file
poem_analyzer.save_response_to_json_file(response)