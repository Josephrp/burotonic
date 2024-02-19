# ./src/mappers/team.py
import openai

class teammappers:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def get_completion(self, user_input, temperature=1, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0):
        messages = [
            {
                "role": "system",
                "content": "You are a subject matter technical expert. You select ONLY ONE from the list provided. ALWAYS respond in complete JSON. Always respond with the best possible team selected with YES or NO. ONLY\r\nselect ONE TEAM:\r\n        \"Team\": {\r\n          \"DefaultTeam\": {\r\n            \"type\": \"boolean\",\r\n            \"description\": \"select this team if the user querry is not related to any of the following teams\"\r\n          },\r\n          \"SalesIntelligence\": {\r\n            \"type\": \"boolean\",\r\n            \"description\": \"select this team if the user is requesting something related to sales intelligence such as client profiles\"\r\n          },\r\n          \"FinanceTeam\": {\r\n            \"type\": \"boolean\",\r\n            \"description\": \"select this team the user requires analysis and advice about financials and financial literature\"\r\n          },\r\n          \"CodingTeam\": {\r\n            \"type\": \"boolean\",\r\n            \"description\": \"select this team if the task requires producing code or technology\"\r\n          },\r\n          \"MarkettingIntelligenceTeam\": {\r\n            \"type\": \"boolean\",\r\n            \"description\": \"select this team if the user requires marketting intelligence activities such as company profiles\"\r\n          },\r\n          \"ConsultingTeam\": {\r\n            \"type\": \"boolean\",\r\n            \"description\": \"select this team if the user requires business consulting\"\r\n          }\r\n        }  }\r\n    }\r\n  }\r\n]   \"required\": [\"DefaultTeam\", \"SalesIntelligence\" , \"FinanceTeam\", \"CodingTeam\" , \"MarkettingIntelligenceTeam\" , \"ConsultingTeam\"] "
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return response
# Example Response
# {
#   "role": "assistant",
#   "content": "```json\n{\n  \"Team\": {\n    \"DefaultTeam\": false,\n    \"SalesIntelligence\": false,\n    \"FinanceTeam\": false,\n    \"CodingTeam\": true,\n    \"MarkettingIntelligenceTeam\": false,\n    \"ConsultingTeam\": false\n  }\n}\n```"
# }