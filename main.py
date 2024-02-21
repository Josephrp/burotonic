# ./main.py
import os
import sys
from dotenv import load_dotenv
from autogen import GroupChat, GroupChatManager
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from src.mappers.team import teamMappers
from src.agentics.agentcreate import agentCreator
import autogen
from autogen.util import load_config, get_openai_keys

# Append the config directory to sys.path for importing config functionalities
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'config'))

# Load environment variables
dotenv_system_messages_path = os.path.join(os.path.dirname(__file__), 'src', 'promptburo', 'system_messages.env')
dotenv_assistants_env_path = os.path.join(os.path.dirname(__file__), 'src', 'config', 'assistants.env')
load_dotenv(dotenv_system_messages_path)
load_dotenv(dotenv_assistants_env_path)
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'OAI_CONFIG.json')
config = load_config(config_path)
openai_keys = get_openai_keys(config)
if openai_keys:
    openai_key = openai_keys[0]
    print(f"Using OpenAI key: {openai_key}")
else:
    raise ValueError("No OpenAI API keys found in the configuration.")

# Initialize TeamMapper and AgentCreator with API key
team_mapper = teamMappers(openai_key)
agent_creator = agentCreator(openai_key)

# Load configuration list for Autogen
config_list = config_list_from_json(os.path.join(os.path.dirname(__file__), '..', 'config', 'OAI_CONFIG_LIST_sample.json'))

# Function to create a GPT agent on-the-fly based on input criteria
def create_dynamic_agent(name, role):
    assistant_id = agent_creator.create_agent(name=name, role=role)
    return GPTAssistantAgent(name=name, llm_config={"config_list": config_list, "assistant_id": assistant_id})

# Function to manage team composition and interaction
def manage_teams(user_input):
    team = team_mapper.map_team(user_input)
    print(f"Selected Team: {team}")

    # Example Teams and their corresponding actions
    teams_functions = {
        "DefaultTeam": lambda: [
            create_dynamic_agent("Default Assistant", "Handling default tasks")
        ],
        # Add more teams and their corresponding dynamic agents creation logic
    }

    if team not in teams_functions:
        print("No specific team mapped, using DefaultTeam.")
        team = "DefaultTeam"

    # Create Autogen GroupChat with the dynamically created agent(s)
    agents = teams_functions[team]()
    groupchat = GroupChat(agents=agents, messages=[], max_round=15)
    group_chat_manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})
    group_chat_manager.start()

def main():
    user_input = "I need help understanding Autogen library."
    manage_teams(user_input)

if __name__ == "__main__":
    main()