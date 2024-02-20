# agentbuilder.py
import os
from dotenv import load_dotenv
from systemprompt import SystemPrompt
from agentcreate import AgentCreator

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), 'config', 'assistants.env')
load_dotenv(dotenv_path)

def build_agent_from_input(user_input):
    # Initialize SystemPrompt with IDs from environment variables or hardcoded values
    IMPROVEINPUT_ID = os.getenv("IMPROVEINPUT_ID")
    SYSTEMPROMPT_ID = os.getenv("SYSTEMPROMPT_ID")
    system_prompt_processor = SystemPrompt(IMPROVEINPUT_ID, SYSTEMPROMPT_ID)
    
    # Process the user input through the system prompt
    processed_output = system_prompt_processor.process_input(user_input)
    print("Processed Output:", processed_output)
    
    # Initialize AgentCreator with API key from environment variables or hardcoded value
    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_api_key_here")
    agent_creator = AgentCreator(api_key=OPENAI_API_KEY)
    
    # Use the processed output as instructions to create a new assistant
    assistant_response = agent_creator.create_assistant(
        name="Generated Assistant",
        instructions=processed_output,
        tools=[{"type": "code_interpreter"}],  # Adjust tools as needed
        model="gpt-4-turbo-preview"  # Adjust model as needed
    )
    
    # Extract and print the assistant ID
    if assistant_response:
        assistant_id = assistant_response.get('id', None)
        print(f"Assistant ID: {assistant_id}")
    else:
        print("Failed to create assistant.")

# if __name__ == "__main__":
#     user_input = input("Please enter your query to build an agent: ")
#     build_agent_from_input(user_input)
