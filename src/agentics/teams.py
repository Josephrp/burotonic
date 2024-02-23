# File: ./src/agentics/teams.py
import os
from dotenv import load_dotenv
from autogen import GroupChat, GroupChatManager
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import config_list_from_json
from src.agentics.agentcreate import agentCreator
import src.promptburo

class TeamManager:
    def __init__(self, openai_key="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"):
        # Load environment variables for assistant IDs, system messages, and teams
        dotenv_path_system_messages = os.path.join(os.getcwd(), 'src', 'promptburo', 'system_messages.env')
        dotenv_path_assistants = os.path.join(os.getcwd(), 'src', 'config', 'assistants.env')
        dotenv_path_teams = os.path.join(os.getcwd(), 'src', 'promptburo', 'teams.env')
        
        load_dotenv(dotenv_path_system_messages)
        load_dotenv(dotenv_path_assistants)
        load_dotenv(dotenv_path_teams)
        
        self.agent_creator = agentCreator(openai_key)
        self.config_list = config_list_from_json(os.path.join(os.getcwd(), '..', 'config', 'OAI_CONFIG_LIST_sample.json'))

        self.team_agents = self._load_teams_config()

    def _load_teams_config(self):
        teams_config = {}
        for key in os.environ:
            if key in ["DefaultTeam", "SalesIntelligence", "FinanceTeam", "CodingTeam", "MarketingIntelligenceTeam", "ConsultingTeam"]:
                teams_config[key] = os.getenv(key).split(',')
        return teams_config

    def create_agent(self, role):
        assistant_id = os.getenv(f"{role.upper()}_ASSISTANT_ID")
        system_message = os.getenv(f"{role.upper()}_MESSAGE")
        if not assistant_id:
            raise ValueError(f"Assistant ID not found for role: {role}")
        return GPTAssistantAgent(name=role, llm_config={"config_list": self.config_list, "assistant_id": assistant_id}, initial_msg=system_message)

    def manage_teams(self, team, user_input):
        agents = []

        # Dynamically create agents based on the team's roles
        if team in self.team_agents:
            for role in self.team_agents[team]:
                agents.append(self.create_agent(role))
        else:
            print(f"No specific team mapped or team not recognized: {team}, using DefaultTeam.")
            for role in self.team_agents.get("DefaultTeam", []):
                agents.append(self.create_agent(role))
        
        # Create Autogen GroupChat with the created agents
        groupchat = GroupChat(agents=agents, messages=[], max_round=15, user_initiated_content=user_input)
        group_chat_manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": self.config_list})
        group_chat_manager.start()

        return group_chat_manager
# # Example usage (Note: adjust the paths and configuration as needed)
# if __name__ == "__main__":
#     team_manager = TeamManager("your_openai_key_here")
#     team_chosen = "CodingTeam"  # Example team chosen
#     user_input = "I need help with a Python project."
#     team_manager.manage_teams(team_chosen, user_input)

tezor=TeamManager()