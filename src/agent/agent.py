from llm.prompt import build_agent_system_prompt
from llm.openrouter import OpenRouterAPI
from agent.tools.web_search import WebSearchTool
from agent.tools.python_executor import PythonExecutorTool
from agent.parser import agent_format_response
from logger import get_logger
from memory.memory_manager import (
    initialize_conversation,
    get_context,
    append_to_conversation,
)
import json
from agent.tools.base import BaseTool
from core.config import setting

class Agent:
    def __init__(self, llm_api: OpenRouterAPI = None):
        self.logger = get_logger("agent")
        self.llm_api = llm_api if llm_api is not None else OpenRouterAPI()
        self.tools: dict[str, BaseTool] = {}
        self.max_steps = setting.AGENT_MAX_STEP  # Maximum number of steps the agent can take

    def register_tool(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get_registered_tools(self):
        return list(self.tools.keys())

    def get_tool(self, tool_name: str):
        return self.tools.get(tool_name, None)

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
            {
                "role": "system",
                "content": build_agent_system_prompt(self.tool_definitions),
            },
            *get_context(conversation_id),
        ]
        for i in range(self.max_steps):
            self.logger.info(
                f"Step {i + 1}/{self.max_steps}: Sending messages to OpenRouter API."
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
                    tool.validate(args=tool_args)

                    self.logger.info(
                        f"Executing tool: {tool_name} with args: {tool_args}"
                    )
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
        self.logger.warning(
            "Sorry, I couldn't complete the task within the step limit."
        )
        return


agent = Agent(llm_api=OpenRouterAPI())

agent.register_tool(PythonExecutorTool())
agent.register_tool(WebSearchTool())
