from exceptions import ParserError, ToolExecutionError, ToolExecutionError, ToolNotFoundError, ToolValidationError
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
from agent.state import AgentState
from agent.tool_executer import ToolExecutor
from agent.llm_runner import LLMRunner
from agent.response_handler import ResponseHandler

class Agent:
    def __init__(self, llm_api: OpenRouterAPI = None):
        self.logger = get_logger("agent")
        self.llm_api = llm_api if llm_api is not None else OpenRouterAPI()
        self.tools: dict[str, BaseTool] = {}
        self.max_steps = (
            setting.AGENT_MAX_STEP
        ) # Maximum number of steps the agent can take
        self.response_handler = ResponseHandler()
        self.tool_executor = ToolExecutor(tools=self.tools)
        self.llm_runner = LLMRunner(llm=self.llm_api)


    def register_tool(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get_registered_tools(self):
        return list(self.tools.keys())

    def get_tool(self, tool_name: str):
        return self.tools.get(tool_name, None)
    
    def initialize_state(self, user_input: str, conversation_id: str) -> AgentState:

        state = AgentState(conversation_id=conversation_id, user_input=user_input)
        return state

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
    
    def execute_action(self, state:AgentState, parsed_response: dict, conversation_id: str):
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
                        conversation_id=conversation_id,
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
                except ToolNotFoundError as e:
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
    def run(self, user_input, conversation_id: str):

        state = self.initialize_state(user_input, conversation_id)

        append_to_conversation(
            role="user", content=user_input, conversation_id=conversation_id
        )
        state.messages = [
            {
                "role": "system",
                "content": build_agent_system_prompt(self.tool_definitions),
            },
            *get_context(conversation_id),
        ]
        # for i in range(self.max_steps):
        while not state.finished and state.current_step < self.max_steps: 
            self.logger.info(
                f"Step {state.current_step + 1}/{self.max_steps}: Sending messages to OpenRouter API."
            )
            self.logger.info("Calling OpenRouter API...")

            llm_response = self.llm_runner.run(messages=state.messages)

            self.logger.info(f"llm response in agent, {llm_response}")

            try:
                parsed_response = self.response_handler.parse(llm_response, conversation_id, state, self.logger)
            except:
                continue  # Skip to the next iteration to get a new response

            self.logger.info(f"Parsed llm response: {parsed_response}")

            step_outcome = self.execute_action(state, parsed_response, conversation_id)
            if state.finished:
                return step_outcome
            else:
                state.current_step += 1
                continue

        self.logger.warning(
            "Sorry, I couldn't complete the task within the step limit."
        )
        return


agent = Agent(llm_api=OpenRouterAPI())

agent.register_tool(PythonExecutorTool())
agent.register_tool(WebSearchTool())
