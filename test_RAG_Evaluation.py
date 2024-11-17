import time

import pandas as pd

from ALLaM_Manager import Manager
from ALLaM_RAG import RAG

rag = RAG()
user_input = rag.questions_for_evaluation()
references = rag.referenced_answer_for_evaluation()

token_manager = Manager()
access_token = token_manager.get_access_token()

data = []
for i in range(len(user_input)):

    if i % 10 == 0:
        time.sleep(10)
        # Initialize TokenManager and get the token
        access_token = token_manager.get_access_token()

    # Initialize ALLaMQueryHandler
    rag = RAG(access_token, user_input[i])

    data.append(rag.evaluation_data(user_input[i], references[i]))

evaluation_df = pd.DataFrame(data)

rag.save_evaluation_data_to_json_file(evaluation_df)
print(evaluation_df)
