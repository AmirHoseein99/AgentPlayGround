import subprocess
import sys

def python_executor_tool(code: str) -> str:
    """
    Executes the given Python code and returns the output as a string.
    """
    try:
        result = subprocess.run([sys.executable, "-c", code], check=True, capture_output=True, text=True, timeout=10)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing code: {e}"