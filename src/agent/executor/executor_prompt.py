import json
from pathlib import Path


def build_step_executor_system_prompt(tool_definitions: list[dict]) -> str:
    tools_text = "\n\n".join(
        f"""Tool Name: {tool["name"]}
            Description: {tool["description"]}
            Schema:
            {json.dumps(tool["schema"], indent=2)}"""
            
            for tool in tool_definitions
    )
    template = Path(
        "src/llm/prompts/executor.txt"
    ).read_text()

    return template.replace(
        "{tools_text}",
        tools_text
    )