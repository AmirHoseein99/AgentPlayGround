from ..llm.prompt import SYSTEM_PROMPT
from ..llm.openrouter import OpenRouterAPI
from .parser import agent_format_response
from .tools.web_search import web_search_tool
from .tools.python_executor import python_executor_tool



tool_calling = {
    'web_search': web_search_tool,
    'python_executor': python_executor_tool
}


def call_agent(user_input):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    llm_api = OpenRouterAPI()
    while True : 
        print("Calling OpenRouter API...")
        llm_response = llm_api.call_openrouter_api(messages=messages)
        print("Received response from OpenRouter API.")
        parsed_response = agent_format_response(llm_response)
        print(f"Parsed response: {parsed_response}")
        if parsed_response.get("type") == "final" : 
            print("Final response received from agent.")
            return parsed_response.get("content")
  
        elif parsed_response.get('type') == 'tool_call' : 
            # return 'Tool calling is not implemented yet.'
            #Note: The agent is requesting to call a tool. You would need to implement the logic to handle this based on your specific tools and requirements.
            print("Tool call detected in agent response.")
            tool_name = parsed_response.get('tool')
            tool_args = parsed_response.get('args')
            print(f"Tool call detected: {tool_name} with args {tool_args}")
            # Here you would implement the logic to call the appropriate tool based on tool_name and tool_args
            # For demonstration, let's assume we have a function call_tool that takes care of this
            try : 
                tool = tool_calling.get(tool_name, None)
                if tool is None:
                    print(f"Tool not found: {tool_name}")
                    continue
                tool_result = tool(**tool_args)
            except Exception as e:
                print(f"Error occurred while calling tool {tool_name}: {e}")
                tool_result = f"An error occurred while calling tool {tool_name}: {e}"
            print(f"Tool result: {tool_result}")
            # Append the tool result to messages for the next iteration
            messages.append({"role": "assistant", "content": str(parsed_response)})
            messages.append({"role": "system", "content": f"Tool result for {tool_name}: {tool_result}"})

    
