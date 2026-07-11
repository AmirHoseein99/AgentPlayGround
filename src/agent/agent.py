
from src.agent.executor.step_executor import StepExecutor
from src.llm.openrouter import OpenRouterAPI
from src.agent.tools.web_search import WebSearchTool
from src.agent.tools.python_executor import PythonExecutorTool
from src.logger import get_logger
from src.agent.tools.base import BaseTool
from src.core.config import setting
from src.agent.state import AgentState
from src.agent.tool_executer import ToolExecutor
from src.agent.llm_runner import LLMRunner
from src.agent.action_executer import ActionExecutor
from src.agent.planner.planner import Planner
from src.memory.memory_manager import append_to_conversation, initialize_conversation

class Agent:
    def __init__(self, llm_api: OpenRouterAPI = None):
        self.logger = get_logger("agent")
        self.llm_api = llm_api if llm_api is not None else OpenRouterAPI()
        self.tools: dict[str, BaseTool] = {}
        self.max_steps = (
            setting.AGENT_MAX_STEP
        )  # Maximum number of steps the agent can take
        
        self.tool_executor = ToolExecutor(tools=self.tools)
        self.llm_runner = LLMRunner(llm=self.llm_api)
        self.action_executor = ActionExecutor(tools=self.tools)
        self.planner = Planner()

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

    def run(self, user_input, conversation_id: str):
        
        initialize_conversation(conversation_id)
        append_to_conversation(conversation_id=conversation_id, role="user", content=user_input)
        
        state = self.initialize_state(user_input, conversation_id)
        state.plan = self.planner.produce_plan(user_input=user_input)
        
        append_to_conversation(conversation_id=conversation_id, role="system", content=f"Planning completed with {len(state.plan.steps)} steps")
        
        
        results = {}
        
        self.setp_executor= StepExecutor(
            tool_definitions=self.tool_definitions,
            tools=self.tools
        )
        
        for step in state.plan.steps:
            append_to_conversation(conversation_id=conversation_id, role="system", content=f"Plan step : {step}")
            if all(results.get(dep_id) is not None for dep_id in step.depends_on):
                result = self.setp_executor.execute_step(step, results, state)
                results[step.id] = result
            else:
                self.logger.warning(f"Step {step.id} dependencies not met, skipping")
                continue

        self.logger.warning(
            "Sorry, I couldn't complete the task within the step limit."
        )
        return


agent = Agent(llm_api=OpenRouterAPI())

agent.register_tool(PythonExecutorTool())
agent.register_tool(WebSearchTool())
