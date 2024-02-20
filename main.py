# ./main.py

import os
from dotenv import load_dotenv


# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), 'src', 'promptburo', 'system_messages.env')
load_dotenv(dotenv_path)
dotenv_path = os.path.join(os.path.dirname(__file__), 'src', 'config', 'assistants.env')
load_dotenv(dotenv_path)

# # Now, os.environ will contain the variables defined in assistants.env
# RESEARCHER_ASSISTANT_ID = os.getenv('RESEARCHER_ASSISTANT_ID')
# RESEARCH_MANAGER_ASSISTANT_ID = os.getenv('RESEARCH_MANAGER_ASSISTANT_ID')
# DIRECTOR_ASSISTANT_ID = os.getenv('DIRECTOR_ASSISTANT_ID')


# # Accessing a variable
# CODER_MESSAGE = os.getenv('CODER_MESSAGE')