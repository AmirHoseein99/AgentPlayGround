from agent.agent import Agent
from agent.tools.web_search import WebSearchTool

class FakeLLM:
    def call_openrouter_api(self, messages):
        return {
            "choices": [{
                "message": {
                    "content": '{"type":"final","response":"hello", "tool":null,"args":null}'
                }
            }]
        }
    
def test_agent_final_response():
    agent = Agent(llm_api=FakeLLM())

    agent.register_tool(WebSearchTool())

    result = agent.run("hi", "conv1")
    print(result)
    assert result == "hello"