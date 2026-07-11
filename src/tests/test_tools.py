from src.agent.tools.web_search import WebSearchTool
from src.agent.tools.python_executor import PythonExecutorTool
from src.agent.tools.web_search import WebSearchTool
from unittest.mock import Mock, patch





@patch("src.agent.tools.web_search.TavilyClient")
def test_web_search_tool(mock_client):
    mock_instance = Mock()
    mock_instance.search.return_value = {
        "results": [
            {"title": "Hello", "content": "World"}
        ]
    }

    mock_client.return_value = mock_instance

    tool = WebSearchTool()
    result = tool.execute(query="hello")

    assert result is not None


def test_python_executor_tool():

    tool = PythonExecutorTool()

    code = "result = 1 + 1"
    result = tool.execute(code=code)

    assert result == 2
