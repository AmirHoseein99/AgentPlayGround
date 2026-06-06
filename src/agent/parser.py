
import ast

def agent_format_response(response):
    if "choices" in response and len(response["choices"]) > 0:
        str_response = str(response["choices"][0]["message"]["content"])
        return ast.literal_eval(str_response)
    else:
        raise Exception("Invalid response format from OpenRouter API")