# Import necessary libraries
# Assuming the API client library is available and configured for authentication
# This is a placeholder import, replace it with your actual client library import
from openai import OpenAI

class AssistantRun:
    def __init__(self, assistant_id):
        self.client = OpenAI() 
        self.assistant_id = assistant_id

    def create_thread(self):
        """Create a new thread."""
        thread = self.client.beta.threads.create()
        return thread

    def add_message_to_thread(self, thread_id, content, role="user"):
        """Add a message to a specific thread."""
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=content
        )
        return message

    def run_assistant(self, thread_id, instructions=None):
        """Run the assistant for a specific thread, with optional instructions."""
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
            instructions=instructions
        )
        return run

    def check_run_status(self, thread_id, run_id):
        """Check the status of a run."""
        run_status = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        return run_status

    def get_messages(self, thread_id):
        """Retrieve messages from a thread."""
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id
        )
        return messages

    def execute(self, user_message, instructions=None):
        """Execute the full flow: create thread, add message, run assistant, and get response."""
        thread = self.create_thread()
        self.add_message_to_thread(thread.id, user_message)
        run = self.run_assistant(thread.id, instructions)
        
        # Assuming the API or your client has a way to wait for or check the completion
        # This might need to be replaced with a more appropriate method for your setup
        run_status = self.check_run_status(thread.id, run.id)
        while run_status.status != 'completed':
            run_status = self.check_run_status(thread.id, run.id)
        
        messages = self.get_messages(thread.id)
        return messages

# # Example usage
# if __name__ == "__main__":
#     assistant_id = "asst_UMcL08TCFXFAHiGnqU3j6ncH"
#     agent = AgentBuilder(assistant_id)
#     user_message = "I need to solve the equation `3x + 11 = 14`. Can you help me?"
#     instructions = "Please address the user as Jane Doe. The user has a premium account."
    
#     response_messages = agent.execute(user_message, instructions)
#     for message in response_messages['data']:
#         print(f"ROLE: {message['role']}\nCONTENT: {message['content']}\n")
