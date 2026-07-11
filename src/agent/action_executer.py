from src.agent.tools.base import BaseTool
from src.agent.tool_executer import ToolExecutor
from src.agent.state import AgentState
from src.logger import get_logger
from src.exceptions import ToolNotFoundError, ToolValidationError, ToolExecutionError
from src.memory.memory_manager import append_to_conversation
import json


class ActionExecutor:
    def __init__(self, tools: dict[str, BaseTool]):
        self.tool_executor = ToolExecutor(tools)
        self.logger = get_logger("action_executor")

    def execute_action(
        self, state: AgentState, parsed_response: dict,
    ):
        # --------------------
        # FINAL RESPONSE
        # --------------------
        if parsed_response.get("type") == "final":
            self.logger.info(f"Agent Final Response : {parsed_response}")
            state.final_answer = parsed_response.get("message")
            state.finished = True
            return parsed_response["message"]
        # --------------------
        # TOOL CALL
        # --------------------
        if parsed_response.get("type") == "tool_call":
            try:
                tool_name = parsed_response.get("tool")
                tool_args = parsed_response.get("args")

                tool_result = self.tool_executor.execute(tool_name, tool_args)
                state.tool_results.append(
                    {
                        "tool": tool_name,
                        "args": tool_args,
                        "result": tool_result,
                    }
                )
                append_to_conversation(
                    role="tool",
                    content=tool_result,
                    conversation_id=state.conversation_id,
                    tool_name=tool_name,
                )
                state.messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(
                            {"tool": tool_name, "result": tool_result}
                        ),
                    }
                )
            except ToolNotFoundError:
                self.logger.error(f"Tool not found: {parsed_response.get('tool')}")
                state.messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(
                            {
                                "tool": parsed_response.get("tool"),
                                "result": f"tool {parsed_response.get('tool')} not found",
                            }
                        ),
                    }
                )
            except ToolValidationError as e:
                self.logger.error(f"Tool validation error: {e}")
                state.messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(
                            {
                                "tool": parsed_response.get("tool"),
                                "result": f"tool {parsed_response.get('tool')} validation error: {e}",
                            }
                        ),
                    }
                )
            except ToolExecutionError as e:
                self.logger.error(f"Tool execution error: {e}")
                state.messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(
                            {
                                "tool": parsed_response.get("tool"),
                                "result": f"tool {parsed_response.get('tool')} execution error: {e}",
                            }
                        ),
                    }
                )
