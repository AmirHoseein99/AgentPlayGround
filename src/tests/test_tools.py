from agent.tools.web_search import WebSearchTool
from agent.tools.python_executor import PythonExecutorTool

def test_web_search_tool():
    tool = WebSearchTool()

    result = tool.execute(query="hello")
    assert result is not None

def test_python_executor_tool():

    tool = PythonExecutorTool()

    code = "result = 1 + 1"
    result = tool.execute(code=code)

    assert result == 2