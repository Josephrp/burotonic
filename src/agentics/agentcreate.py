# ./src/agentics/agentcreate.py

import openai
import json
import os

class agentCreator:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def create_assistant(self, instructions, model, tools, name = "Tonic"):
        """
        Create an assistant with the specified parameters.
        """
        try:
            response = openai.Assistant.create(
                name=name,
                instructions=instructions,
                tools=tools,
                model=model
            )
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def parse_response_to_json(self, response_str):
        """
        Parse the response string to JSON and return the assistant ID.
        """
        try:
            response_json = json.loads(response_str)
            assistant_id = response_json.get('id', None)
            return assistant_id
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return None
# yt=agentCreator()
# yt.create_assistant("fin","you are a finance expert",)

# example response 


# {"id":"asst_5JUroVHGMb2uJgIYP9jtdS3D","object":"assistant","created_at":1708458950,"name":null,"description":null,"model":"gpt-4-turbo-preview","instructions":"You are a personal math tutor. When asked a math question, write and run code to answer the question.","tools":[{"type":"code_interpreter"}],"file_ids":[],"metadata":{}}

# # Example usage
# if __name__ == "__main__":
#     # Replace 'your_api_key_here' with your actual OpenAI API key
#     api_key = os.getenv("OPENAI_API_KEY", "your_api_key_here")
#     agent_creator = AgentCreator(api_key=api_key)

#     # Create an assistant
#     assistant_response = agent_creator.create_assistant(
#         name="Math Tutor",
#         instructions="You are a personal math tutor. Write and run code to answer math questions.",
#         tools=[{"type": "code_interpreter"}],
#         model="gpt-4-turbo-preview"
#     )

#     if assistant_response:
#         # Convert the response to a string to simulate receiving a string response
#         response_str = json.dumps(assistant_response)
#         # Parse the response and print the assistant ID
#         assistant_id = agent_creator.parse_response_to_json(response_str)
#         print(f"Assistant ID: {assistant_id}")
#     else:
#         print("Failed to create assistant.")
