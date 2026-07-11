import json

from src.agent.llm_runner import LLMRunner
from src.agent.planner.models import ExecutionPlan
from src.llm.openrouter import OpenRouterAPI
from src.logger import get_logger
from src.agent.planner.planner_prompt import build_planner_prompt

class Planner :
    def __init__(self):
        
        self.llm = LLMRunner(llm=OpenRouterAPI())
        self.logger = get_logger("planner")
        self.plan = None

    def produce_plan(self, user_input: str):

        prompt = build_planner_prompt(user_input=user_input)

        self.logger.info(f"Generating plan for input: {user_input}")
        response = self.llm.run(messages=[{"role": "system", "content": prompt}], caller="planner")
        self.plan = response['choices'][0]['message']['content']

        data = json.loads(self.plan)

        return ExecutionPlan.model_validate(data)