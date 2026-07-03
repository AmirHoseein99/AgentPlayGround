import subprocess
import sys
from ...logger import get_logger
from .base import BaseTool


class PythonExecutorTool(BaseTool):
    name = "python_executor"
    description = "A tool for executing Python code."
    schema = {
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "The Python code to execute."},
        },
        "required": ["code"],
    }

    def execute(self, code: str) -> str:
        logger = get_logger("python_executor_tool")
        logger.info(f"Executing Python code: {code}")
        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            logger.info(f"Execution result: {result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.exception(f"Error executing code: {e}")
            return f"Error executing code: {e}"
