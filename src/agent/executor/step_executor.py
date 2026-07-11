import json

from src.agent.action_executer import ActionExecutor
from src.agent.executor.executor_prompt import build_step_executor_system_prompt
from src.agent.llm_runner import LLMRunner
from src.agent.response_handler import ResponseHandler
from src.agent.state import AgentState
from src.llm.openrouter import OpenRouterAPI
from src.logger import get_logger
from src.agent.planner.models import PlanStep, StepStatus
from src.exceptions import PlanExecutionError

class StepExecutor:
    def __init__(self, tool_definitions, tools):
        self.logger = get_logger("plan_executor")
        self.llm_runner = LLMRunner(llm=OpenRouterAPI())
        self.tool_definitions = tool_definitions
        self.executor_system_prompt = build_step_executor_system_prompt(tool_definitions=tool_definitions)
        self.response_handler = ResponseHandler()
        self.action_exectutor = ActionExecutor(tools=tools)
    def execute_step(self, step: PlanStep, results: dict, state: AgentState) -> str:
        self.logger.info(f"Executing step {step.id}: {step.description}")
        try:
            messages = [
                    {"role": "system", "content": self.executor_system_prompt},
                    {"role": "user", "content": json.dumps(step.model_dump())},
                    {"role": "assistant", "content": json.dumps({k: results[k] for k in step.depends_on})}
                ]

            step_execution_detail = self.llm_runner.run(
                messages=messages,
                caller="executor",
            )

            parsed_response = self.response_handler.parse(
                step_execution_detail, state
            )

            print("parsee_plan_execution_path : ", parsed_response)
            
            result = self.action_exectutor.execute_action(state=state, parsed_response=parsed_response)
            print('step Execution Result : ', result)
            step.status = StepStatus.COMPLETED
            return result
        except Exception as e:
            step.status = StepStatus.FAILED
            self.logger.error(f"Step {step.id} failed: {e}")
            raise PlanExecutionError(str(e))
