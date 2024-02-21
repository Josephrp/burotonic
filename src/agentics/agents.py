# ./src/agentics/agents.py

import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb


# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), 'src', 'promptburo', 'system_messages.env')
load_dotenv(dotenv_path)
dotenv_path = os.path.join(os.path.dirname(__file__), 'src', 'config', 'assistants.env')
load_dotenv(dotenv_path)

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    file_location="./src/config/",
    filter_dict={
        "model": ["gpt-3.5-turbo", "gpt-35-turbo", "gpt-35-turbo-0613", "gpt-4", "gpt4", "gpt-4-32k"],
    },
)

print("LLM models: ", [config_list[i]["model"] for i in range(len(config_list))])

llm_config = {
         "timeout": 60,
         "cache_seed": 42,
         "config_list": config_list,
         "temperature": 0,
     }

def termination_msg(self, x):
        return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

class Agents:
    def __init__(self, llm_config, db_path):
        self.llm_config = llm_config
        self.db_path = db_path

    def tonic(self) :
        return autogen.UserProxyAgent(
            name="Boss",
            is_termination_msg=termination_msg,
            human_input_mode="NEVER",
            system_message="The boss who asks questions and gives tasks.",
            code_execution_config=False,
            default_auto_reply="Reply `TERMINATE` if the task is done.",
        )

    # Create the RetrieveUserProxyAgent (Boss Assistant)
    def scitonic(self) :
        return RetrieveUserProxyAgent(
            name="Boss_Assistant",
            is_termination_msg=termination_msg,
            system_message="Assistant who has extra content retrieval power for solving difficult problems.",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
            retrieve_config={
                "task": "QuoraRetrieval",
                "docs_path": self.db_path,
                "chunk_token_size": 1000,
                "model": llm_config["config_list"][0]["model"],
                "client": chromadb.PersistentClient(path="/tmp/chromadb"),
                "collection_name": "groupchat",
                "get_or_create": True,
            },
            code_execution_config=False,
        )
    # Placeholder definitions for agents used in team functions
    def coder(self) : 
        return AssistantAgent(
            name="Coder",
            system_message=os.getenv('CODER_MESSAGE'),
            llm_config=llm_config
        )

    def pm(self) :
        return AssistantAgent(
            name="Project_Manager",
            system_message=os.getenv('PROJECT_MANAGER_MESSAGE'),
            llm_config=llm_config
        )

    def reviewer(self) :
        return AssistantAgent(
            name="Reviewer",
            system_message=os.getenv('REVIEWER_MESSAGE'),
            llm_config=llm_config
        )

    # Define more agents for each team
    def finance_expert(self) :
        return AssistantAgent(
            name="Finance_Expert",
            system_message=os.getenv('FINANCE_EXPERT_MESSAGE'),
            llm_config=llm_config
        )

    def debate_champion(self) :
        return AssistantAgent(
            name="Debate_Champion",
            system_message=os.getenv('DEBATE_CHAMPION_MESSAGE'),
            llm_config=llm_config
        )

    def academic_whiz(self) :
        return AssistantAgent(
        name="Academic_Whiz",
        system_message=os.getenv('ACADEMIC_WHIZ_MESSAGE'),
        llm_config=llm_config
    )

    def consulting_pro(self) :
            return AssistantAgent(
            name="Consulting_Pro",
            system_message=os.getenv('CONSULTING_PRO_MESSAGE'),
            llm_config=llm_config
        )
    def covid19_scientist(self) : 
        return AssistantAgent(
            name="Covid19_Scientist",
            system_message=os.getenv('COVID19_SCIENTIST_MESSAGE'),
            llm_config=llm_config
        )

    def healthcare_expert(self) : 
        return AssistantAgent(
            name="Healthcare_Expert",
            system_message=os.getenv('HEALTHCARE_EXPERT_MESSAGE'),
            llm_config=llm_config
        )

    def finance_analyst(self) :
        return AssistantAgent(
            name="Finance_Analyst",
            system_message=os.getenv('FINANCE_ANALYST_MESSAGE'),
            llm_config=llm_config
        )

    def debate_expert(self) :
        return AssistantAgent(
            name="Debate_Expert",
            system_message=os.getenv('DEBATE_EXPERT_MESSAGE'),
            llm_config=llm_config
        )

    def academic_expert(self) :
        return AssistantAgent(
            name="Academic_Expert",
            system_message="os.getenv('ACADEMIC_EXPERT_MESSAGE'),
            llm_config=llm_config
        )

### Load Assistants

# Create researcher agent
researcher = GPTAssistantAgent(
    name = "researcher",
    llm_config = {
        "config_list": config_list,
        "assistant_id": RESEARCHER_ASSISTANT_ID
    }
)

# Create research manager agent
research_manager = GPTAssistantAgent(
    name="research_manager",
    llm_config = {
        "config_list": config_list,
        "assistant_id": RESEARCH_MANAGER_ASSISTANT_ID
    }
)

# Create director agent
director = GPTAssistantAgent(
    name = "director",
    llm_config = {
        "config_list": config_list,
        "assistant_id": DIRECTOR_ASSISTANT_ID,
    }
)


# Create director agent
profiler = GPTAssistantAgent(
    name = "profiler",
    llm_config = {
        "config_list": config_list,
        "assistant_id": PROFILER_ASSISTANT_ID,
    }
)

# Create director agent
longcontent = GPTAssistantAgent(
    name = "longcontentcreator",
    llm_config = {
        "config_list": config_list,
        "assistant_id": LONGCONTENT_ASSISTANT_ID,
    }
)