import os
import sys
from dotenv import load_dotenv
import autogen
from autogen.util import load_config, get_openai_keys, config_list_from_json
from src.mappers.team import teamMappers
from src.agentics.teams import TeamManager 

# Append the config directory to sys.path for importing config functionalities
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'config'))

# Load environment variables for system messages and assistants
dotenv_system_messages_path = os.path.join(os.path.dirname(__file__), 'src', 'promptburo', 'system_messages.env')
dotenv_assistants_env_path = os.path.join(os.path.dirname(__file__), 'src', 'config', 'assistants.env')
load_dotenv(dotenv_system_messages_path)
load_dotenv(dotenv_assistants_env_path)

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

# Initialize the TeamMapper with the OpenAI API key
team_mapper = teamMappers(openai_key)

# Function to route the user input and manage the interaction based on the mapped team
def route_user_input(user_input):
    # Map user input to a specific team
    team = team_mapper.map_team(user_input)
    print(f"User input routed to the following team: {team}")
    
    # Initialize TeamManager with configuration and API key
    team_manager = TeamManager(openai_key)
    
    # Manage teams and interactions based on the mapped team
    team_manager.manage_teams(team, user_input)

def main():
    # Example user input
    user_input = "I need help understanding Autogen library."
    route_user_input(user_input)

if __name__ == "__main__":
    main()