import pytest
from agent.parser import agent_format_response
from exceptions import ParserError


def test_valid_tool_call():
    response = {
        "choices": [{
            "message": {
                "content": '{"type":"tool_call","tool":"web_search","args":{"query":"hi"}}'
            }
        }]
    }

    result = agent_format_response(response)

    assert result["type"] == "tool_call"
    assert result["tool"] == "web_search"

def test_invalid_json():
    response = {
        "choices": [{
            "message": {
                "content": 'THIS IS NOT JSON'
            }
        }]
    }

    with pytest.raises(ParserError):
        agent_format_response(response)