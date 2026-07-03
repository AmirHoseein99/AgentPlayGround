from ..llm.prompt import AGENT_SYSTEM_PROMPT
from ..llm.openrouter import OpenRouterAPI
from .parser import agent_format_response
from .tools.web_search import web_search_tool
from .tools.python_executor import python_executor_tool
from ..logger import get_logger
from ..memory.memory_manager import (
    initialize_conversation,
    get_context,
    append_to_conversation,
)
import json

tool_calling = {"web_search": web_search_tool, "python_executor": python_executor_tool}

max_steps = 10


def call_agent(user_input, conversation_id: str):

    initialize_conversation(conversation_id=conversation_id)
    append_to_conversation(
        role="user", content=user_input, conversation_id=conversation_id
    )

    logger = get_logger("agent")

    messages = [
        {"role": "system", "content": AGENT_SYSTEM_PROMPT},
        *get_context(conversation_id),
    ]
    llm_api = OpenRouterAPI()

    for i in range(max_steps):
        logger.info(f"Step {i + 1}/{max_steps}: Sending messages to OpenRouter API.")

        logger.info("Calling OpenRouter API...")
        llm_response = llm_api.call_openrouter_api(messages=messages)
        logger.info(f"llm response in agent, {llm_response}")

        try:
            parsed_response = agent_format_response(llm_response)
            append_to_conversation(
                role="assistant",
                content=parsed_response,
                conversation_id=conversation_id,
            )
            messages.append(
                {"role": "assistant", "content": json.dumps(parsed_response)}
            )
        except Exception as e:
            logger.exception(e)
            messages.append(
                {
                    "role": "user",
                    "content": f"""
                        Your previous response could not be parsed.

                        Error:
                        {e}

                        Please produce a valid structured response.
                        """,
                }
            )
            continue

        logger.info(f"Parsed llm response: {parsed_response}")

        # --------------------
        # FINAL RESPONSE
        # --------------------
        if parsed_response.get("type") == "final":
            logger.info(f"Agent Final Response : {parsed_response}")
            return parsed_response["message"]

        # --------------------
        # TOOL CALL
        # --------------------
        if parsed_response.get("type") == "tool_call":
            tool_name = parsed_response.get("tool")
            tool_args = parsed_response.get("args")

            tool = tool_calling.get(tool_name)

            if tool is None:
                logger.error(f"Tool not found: {tool_name}")
                continue
            try:
                if not isinstance(tool_args, dict):
                    raise ValueError(f"tool_args must be dict, got {type(tool_args)}")

                tool_result = tool(**tool_args)
                append_to_conversation(
                    role="tool",
                    content=tool_result,
                    conversation_id=conversation_id,
                    tool_name=tool_name,
                )
                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(
                            {"tool": tool_name, "result": tool_result}
                        ),
                    }
                )
                continue
            except Exception as e:
                logger.exception(e)
                append_to_conversation(
                    role="tool",
                    content=f"Tool execution failed: {e}",
                    conversation_id=conversation_id,
                    tool_name=tool_name,
                )
                messages.append(
                    {"role": "tool", "content": f"Tool execution failed: {e}"}
                )

    logger.warning("Sorry, I couldn't complete the task within the step limit.")
    return
