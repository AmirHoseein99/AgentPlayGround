import requests
import os
from core.config import setting
from llm.prompt import SYSTEM_PROMPT

class OpenRouterAPI:

    def call_openrouter_api(self, user_input_messages):
        url = f"{setting.OPENROUTER_API_BASE_URL}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {setting.OPENROUTER_API_KEY}"
        }
        data = {
            "model": setting.OPUERTER_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input_messages}
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:        
            raise Exception(f"OpenRouter API call failed with status code {response.status_code}: {response.text}")

    def format_response(self, response):
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        else:
            raise Exception("Invalid response format from OpenRouter API")