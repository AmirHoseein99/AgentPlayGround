from asyncio.log import logger

from ..llm.prompt import AGENT_SYSTEM_PROMPT
from ..llm.openrouter import OpenRouterAPI
from .parser import agent_format_response
from .tools.web_search import WebSearchTool
from .tools.python_executor import PythonExecutorTool
from ..logger import get_logger
from ..memory.memory_manager import (
    initialize_conversation,
    get_context,
    append_to_conversation,
)
import json
from .tools.base import BaseTool

max_steps = 10


class Agent:
    def __init__(self):
        self.logger = get_logger("agent")
        self.llm_api = OpenRouterAPI()
        self.tools: dict[str, BaseTool] = {}

    def register_tool(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get_registered_tools(self):
        return list(self.tools.keys())

    def get_tool(self, tool_name: str):
        if tool_name not in self.tools:
            self.logger.error(f"Tool '{tool_name}' not found.")
            return None
        return self.tools.get(tool_name)

    def tool_description(self, tool_name: str):
        tool = self.get_tool(tool_name)
        if tool:
            return tool.description
        else:
            return f"Tool '{tool_name}' not found."

    @property
    def tool_definitions(self):
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "schema": tool.schema,
            }
            for tool in self.tools.values()
        ]

    def run(self, user_input, conversation_id: str):
        initialize_conversation(conversation_id=conversation_id)
        append_to_conversation(
            role="user", content=user_input, conversation_id=conversation_id
        )
        messages = [
            {"role": "system", "content": AGENT_SYSTEM_PROMPT},
            *get_context(conversation_id),
        ]
        for i in range(max_steps):
            self.logger.info(
                f"Step {i + 1}/{max_steps}: Sending messages to OpenRouter API."
            )

            self.logger.info("Calling OpenRouter API...")
            llm_response = self.llm_api.call_openrouter_api(messages=messages)
            self.logger.info(f"llm response in agent, {llm_response}")
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
                self.logger.exception(e)
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
            self.logger.info(f"Parsed llm response: {parsed_response}")
            # --------------------
            # FINAL RESPONSE
            # --------------------
            if parsed_response.get("type") == "final":
                self.logger.info(f"Agent Final Response : {parsed_response}")
                return parsed_response["message"]
            # --------------------
            # TOOL CALL
            # --------------------
            if parsed_response.get("type") == "tool_call":
                tool_name = parsed_response.get("tool")
                tool_args = parsed_response.get("args")

                tool = self.get_tool(str(tool_name))

                if tool is None:
                    self.logger.error(f"Tool not found: {tool_name}")
                    messages.append(
                        {
                            "role": "tool",
                            "content": json.dumps(
                                {
                                    "tool": tool_name,
                                    "result": f"tool {tool_name} not found",
                                }
                            ),
                        }
                    )
                try:
                    # TODO : add a validation for tool's args
                    if not isinstance(tool_args, dict):
                        raise ValueError(
                            f"tool_args must be dict, got {type(tool_args)}"
                        )
                    self.logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
                    tool_result = tool.execute(**tool_args)
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
                    self.logger.exception(e)
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


agent = Agent()

agent.register_tool(PythonExecutorTool())
agent.register_tool(WebSearchTool())
