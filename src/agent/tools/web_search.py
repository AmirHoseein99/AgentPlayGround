# To install: pip install tavily-python
from tavily import TavilyClient
from core.config import setting
from logger import get_logger
from agent.tools.base import BaseTool


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "A tool for performing web searches for recent information."
    schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query."},
        },
        "required": ["query"],
    }

    def execute(self, query: str) -> str:
        logger = get_logger("web_search_tool")
        logger.info(f"Executing web search tool with query: {query}")
        client = TavilyClient(setting.TAVILY_API_KEY)
        try:
            response = client.search(query=query, search_depth="advanced")
            logger.info(f"Web search completed with response: {response}")
            return response

        except Exception as e:
            logger.exception(f"Error occurred during web search: {e}")
            return f"An error occurred during web search: {e}"
