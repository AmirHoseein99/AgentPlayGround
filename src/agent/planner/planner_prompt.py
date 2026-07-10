from pathlib import Path


def build_planner_prompt(user_input: str) -> str:
    template = Path(
        "src/llm/prompts/planner.txt"
    ).read_text()

    return template.replace(
        "{USER_INPUT}",
        user_input
    )