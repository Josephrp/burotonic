# ./src/mappers/team.py
import re
import openai
import json
import os
class TeamMappers:
    def __init__(self, api_key):
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'OAI_CONFIG.json')
        self.config = load_config(config_path)
        self.openai_keys = get_openai_keys(config)
        if openai_keys:
            self.api_key = openai_keys[0]
            print(f"Using OpenAI key: {openai_key}")
        else:
            print("No OpenAI API keys found in the configuration.")
        self.config= {"model": "gpt-3.5-turbo-preview","api_key"}

        self.client = openai.OpenAI(api_key=api_key)

    def get_completion(self, user_input, temperature=1, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0):
        print("inside get_completion")
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
        print("going to generate response")

        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        print("response generated")
        # print(response)
        try:
            print("inside try")
            print(response)
            print(response.choices[0].message.content)
            k=response.choices[0].message.content
            pattern = re.compile(r'"([A-Za-z]+)": true')
            matches = pattern.search(k)
            print("it works")
            true_team = matches.group(1)
            print(true_team)
            return true_team
            # json_content = response.choices[0].message.content
            # print(json_content["Team"])
            # data = json.loads(json_content)
            # print(data)
            # # Find the team set to True
            # true_team = [team for team, value in data['Team'].items() if value]
            # print(true_team)
            # # print(data)
            # response_data = json.loads(response.choices[0].message.content)
            
            # team_data = response_data.get("Team", {})
            # return {"Team": team_data}
        except (KeyError, ValueError, TypeError):
            print("inside except")
            
            return {"error": "Failed to parse response or extract 'Team' data"}

# Example Response
# {
#   "role": "assistant",
#   "content": "```json\n{\n  \"Team\": {\n    \"DefaultTeam\": false,\n    \"SalesIntelligence\": false,\n    \"FinanceTeam\": false,\n    \"CodingTeam\": true,\n    \"MarkettingIntelligenceTeam\": false,\n    \"ConsultingTeam\": false\n  }\n}\n```"
# }