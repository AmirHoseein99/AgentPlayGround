import subprocess
import sys
from ...logger import get_logger


def python_executor_tool(code: str) -> str:
    """
    Executes the given Python code and returns the output as a string.
    """
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
