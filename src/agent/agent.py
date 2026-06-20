from ..llm.prompt import SYSTEM_PROMPT
from ..llm.openrouter import OpenRouterAPI
from .parser import agent_format_response
from .tools.web_search import web_search_tool
from .tools.python_executor import python_executor_tool
from ..logger import get_logger
from ..memory.json_memory import append_to_converstaion

tool_calling = {"web_search": web_search_tool, "python_executor": python_executor_tool}

max_steps = 10


def call_agent(user_input, conversation_history, conversation_id: str):
    logger = get_logger("agent")
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history)
    messages = [{"role": "user", "content": user_input}]
    llm_api = OpenRouterAPI()
    for i in range(max_steps):
        logger.info(f"Step {i + 1}/{max_steps}: Sending messages to OpenRouter API.")
        logger.info("Calling OpenRouter API...")
        llm_response = llm_api.call_openrouter_api(messages=messages)
        logger.info("Received response from OpenRouter API.")
        parsed_response = agent_format_response(llm_response)
        append_to_converstaion(parsed_response, conversation_id)
        logger.info(f"Parsed response: {parsed_response}")

        if isinstance(parsed_response, str):
            logger.info("Final response received from agent.")
            return parsed_response

        elif parsed_response.get("type") == "tool_call":
            logger.info("Tool call detected in agent response.")
            tool_name = parsed_response.get("tool")
            tool_args = parsed_response.get("args")
            logger.info(f"Tool call detected: {tool_name} with args {tool_args}")
            try:
                tool = tool_calling.get(tool_name, None)
                if tool is None:
                    logger.info(f"Tool not found: {tool_name}")
                    continue
                tool_result = tool(**tool_args)
            except Exception as e:
                logger.exception(f"Error occurred while calling tool {tool_name}: {e}")
                tool_result = f"An error occurred while calling tool {tool_name}: {e}, Try another approach or reformulate the query."
            logger.info(f"Tool result: {tool_result}")
            append_to_converstaion(f"{tool_name}: {tool_result}", conversation_id)
            # Append the tool result to messages for the next iteration
            messages.append({"role": "assistant", "content": parsed_response})
            messages.append(
                {
                    "role": "system",
                    "content": f"Tool result for {tool_name}: {tool_result}",
                }
            )

    logger.info("Max steps reached without receiving a final response.")
    return "Sorry, I couldn't complete the task within the step limit."
