# To install: pip install tavily-python
from tavily import TavilyClient
from ...core.config import setting

def web_search_tool(query: str) -> str:
    print(f"Executing web search tool with query: {query}")
    client = TavilyClient(setting.TAVILY_API_KEY)
    try:
        response = client.search(
            query=query,
            search_depth="advanced"
        )
        print(type(response))
        print(f"Web search completed with response: {response}")
        return response
    
    except Exception as e:
        print(f"Error occurred during web search: {e}")
        return f"An error occurred during web search: {e}"
    
