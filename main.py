# ./main.py

import os
from dotenv import load_dotenv


# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), 'src', 'promptburo', 'system_messages.env')
load_dotenv(dotenv_path)
dotenv_path = os.path.join(os.path.dirname(__file__), 'src', 'config', 'assistants.env')
load_dotenv(dotenv_path)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'OAI_CONFIG.json')
config = load_config(config_path)
openai_keys = get_openai_keys(config)
    if openai_keys:
        openai_key = openai_keys[0]
#       print(f"Using OpenAI key: {openai_key}")
    else:
        print("No OpenAI API keys found in the configuration.")
