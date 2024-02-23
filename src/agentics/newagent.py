from autogen.agentchat.conversable_agent import ConversableAgent
from autogen.agentchat.groupchat import GroupChat
from autogen.agentchat.groupchat import GroupChatManager
# from autogen.group_chat_manager import GroupChatManager

# Basic LLM configuration
llm_config = {
    "config_list": [],  # Placeholder for LLM configurations
    "cache_seed": 0,  # Placeholder for cache seed
}

# Create two conversable agents with LLM config
agent1 = ConversableAgent(name="Agent1", llm_config=llm_config)
agent2 = ConversableAgent(name="Agent2", llm_config=llm_config)

# Create a reviewer agent with LLM config
reviewer_agent = ConversableAgent(name="ReviewerAgent", llm_config=llm_config)

# Define allowed speaker transitions for the conversation
allowed_speaker_transitions_dict = {
    agent1: [agent2],  # Agent1 can speak to Agent2
    agent2: [agent1],  # Agent2 can speak to Agent1
    reviewer_agent: [agent1, agent2],  # ReviewerAgent can speak to both Agent1 and Agent2
}

# Create a GroupChat with the agents and allowed transitions
group_chat = GroupChat(
    agents=[agent1, agent2, reviewer_agent],
    messages=[],
    max_round=20,  # Maximum number of rounds for the conversation
    speaker_transitions_dict=allowed_speaker_transitions_dict,  # Add speaker transitions
    is_allowed_graph=True,  # Indicate that the transitions represent allowed interactions
)

# Create the manager for the group chat
class CustomGroupChatManager(GroupChatManager):
    def on_round_end(self, round_num):
        if round_num == 10:
            self.groupchat.agents.append(self.groupchat.agents.pop(2))  # Move reviewer to the end
            print("Reviewer is added to the conversation.")
        super().on_round_end(round_num)

manager = CustomGroupChatManager(
    groupchat=group_chat,
    code_execution_config=False,  # Assuming no code execution is allowed for simplicity
    is_termination_msg=None,  # Assuming no termination message detection is needed for simplicity
)

# Start the conversation between Agent1 and Agent2
agent1.initiate_chat(manager, message="Hello Agent2, how are you?")