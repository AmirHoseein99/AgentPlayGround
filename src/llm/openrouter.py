import requests
from ..core.config import setting
from ..logger import get_logger


class OpenRouterAPI:
    def __init__(self) -> None:
        self.url = f"{setting.OPENROUTER_API_BASE_URL}/chat/completions"
        self.logger = get_logger("openrouter")

    def stream_openrouter_response(self, messages):
        session = requests.sessions.Session()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {setting.OPENROUTER_API_KEY}",
        }
        data = {"model": setting.OPENROUTER_MODEL, "messages": messages, "stream": True}

        with session.post(
            self.url, headers=headers, json=data, stream=True
        ) as response:
            for response_lines in response.iter_lines():
                yield response_lines

    def call_openrouter_api(self, messages):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {setting.OPENROUTER_API_KEY}",
        }
        data = {"model": setting.OPENROUTER_MODEL, "messages": messages}
        self.logger.info(
            f"calling openrouter api with header : {headers}, data : {data}"
        )
        response = requests.post(self.url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.exception(
                f"OpenRouter API call failed with status code {response.status_code}: {response.text}"
            )
            raise Exception(
                f"OpenRouter API call failed with status code {response.status_code}: {response.text}"
            )
