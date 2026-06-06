from encodings.punycode import T
import requests
from ..core.config import setting


class OpenRouterAPI:
    def __init__(self) -> None:
        self.url = f"{setting.OPENROUTER_API_BASE_URL}/chat/completions"
            
    def stream_openrouter_response(self, messages):
        session = requests.sessions.Session()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {setting.OPENROUTER_API_KEY}"
        }
        data = {
            "model": setting.OPENROUTER_MODEL,
            "messages": messages,
            "stream" : True
        }

        with session.post(self.url, headers= headers, json=data, stream=True) as response : 
            for response_lines in response.iter_lines() :
                yield response_lines

    def call_openrouter_api(self, messages):
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {setting.OPENROUTER_API_KEY}"
        }
        data = {
            "model": setting.OPENROUTER_MODEL,
            "messages": messages
        }
        response = requests.post(self.url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:        
            raise Exception(f"OpenRouter API call failed with status code {response.status_code}: {response.text}")
