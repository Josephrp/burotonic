# File: ./src/agentics/systemprompt.py
import openai
from openai import OpenAI
import json
from src.agentics.runassistant import AssistantRun

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', 'config', 'assistants.env')
load_dotenv(dotenv_path)
class SystemPrompt:
    def __init__(self, improve_input_id, system_prompt_id):
        self.improve_input_agent = AssistantRun(improve_input_id)
        self.system_prompt_agent = AssistantRun(system_prompt_id)

    def process_input(self, user_input, instructions=None):
        # First, process the user input with the improve_input assistant
        improved_input = self.improve_input_agent.execute(user_input, instructions)
        
        # Then, pass the output of the first assistant as input to the system_prompt assistant
        final_output = self.system_prompt_agent.execute(improved_input, instructions)
        
        return final_output

# # Example usage
# if __name__ == "__main__":
#     IMPROVEINPUT = "asst_avqzq6509OxnIdijW8kwt9QM"
#     SYSTEMPROMPT = "asst_UMcL08TCFXFAHiGnqU3j6ncH"
    
#     system_prompt_processor = SystemPrompt(IMPROVEINPUT, SYSTEMPROMPT)
    
#     user_input = input("Please enter your query: ")
#     final_response = system_prompt_processor.process_input(user_input)
#     print("Final Response:", final_response)