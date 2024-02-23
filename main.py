import os
import sys
from dotenv import load_dotenv
import autogen
from autogen.util import load_config, get_openai_keys, config_list_from_json
from src.mappers.team import TeamMappers
from src.agentics.teams import TeamManager 
from src.agentics.runassistant import AssistantRun 
# Append the config directory to sys.path for importing config functionalities
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'config'))

# Load environment variables for system messages and assistants
dotenv_system_messages_path = os.path.join(os.path.dirname(__file__), 'src', 'promptburo', 'system_messages.env')
dotenv_assistants_env_path = os.path.join(os.path.dirname(__file__), 'src', 'config', 'assistants.env')
load_dotenv(dotenv_system_messages_path)
load_dotenv(dotenv_assistants_env_path)

def load_openai_keys_and_config():
    # Load OpenAI API key from config
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'OAI_CONFIG.json')
    config = load_config(config_path)
    openai_keys = get_openai_keys(config)
    
    if openai_keys:
        openai_key = openai_keys[0]
    else:
        raise ValueError("No OpenAI API keys found in the configuration.")
    
    # Load configuration list for Autogen
    config_list = config_list_from_json(os.path.join(os.path.dirname(__file__), '..', 'config', 'OAI_CONFIG_LIST_sample.json'))
    
    return openai_key, config_list

def route_user_input(user_input):
    # Load OpenAI API key and config
    openai_key, config_list = load_openai_keys_and_config()
    
    # Initialize the TeamMapper with the OpenAI API key
    team_mapper = TeamMappers(openai_key)
    
    # Preprocess the user input with an assistant specified in assistants.env
    # ASSISTANT_NAME is assumed to be the environmental variable specifying which assistant to use for input preprocessing
    assistant_name = os.getenv('ASSISTANT_NAME', 'IMPROVEINPUT')  # Fallback to 'IMPROVEINPUT' if not set
    improved_input = AssistantRun.run(assistant_name, user_input, openai_key)
    
    # Map the improved user input to a specific team
    team = team_mapper.map_team(improved_input)
    print(f"User input routed to the following team: {team}")
    
    if team == "default":


        pass
    else:
        team_manager = TeamManager(openai_key)
        team_manager.manage_teams(team, improved_input)

# def main():
#     # Example user input
#     user_input = "I need help understanding Autogen library."
#     route_user_input(user_input)

# if __name__ == "__main__":
#     main()