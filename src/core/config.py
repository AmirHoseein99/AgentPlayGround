import os
from dotenv import load_dotenv

load_dotenv()


class Setting(object):
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_API_BASE_URL = os.getenv("OPENROUTER_API_BASE_URL")
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        self.AGENT_MAX_STEP = 5
        self.CONTEXT_WINDOW_SIZE = 10
        self.CONVERSATION_MEMORY_THRESHOLD = 20


setting = Setting()
