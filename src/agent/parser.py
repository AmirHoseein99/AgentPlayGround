import json
from logger import get_logger
from exceptions import ParserError

VALID_TYPES = {"final", "tool_call"}


def check_llm_response(response, logger):
    if "choices" not in response or not response["choices"]:
        logger.error(f"Invalid OpenRouter response: {response}")
        raise ParserError("Invalid OpenRouter Response.")


def parse_json(response, logger):
    try:
        return json.loads(response["choices"][0]["message"]["content"])
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        raise ParserError("Cannot parse LLM response.")


def validate_structure(data, logger):
    if "type" not in data:
        raise ParserError("Missing 'type' field")

    if data["type"] not in VALID_TYPES:
        raise ParserError(f"Invalid type: {data['type']}")

    if data["type"] == "tool_call":
        if "tool" not in data:
            raise ParserError("Missing tool name")
        if "args" not in data:
            raise ParserError("Missing tool args")
        if not isinstance(data["args"], dict):
            raise ParserError("Tool args must be a dict")


def agent_format_response(response):
    logger = get_logger("agent_parser")

    check_llm_response(response, logger)

    content = parse_json(response, logger)

    validate_structure(content, logger)

    logger.info(f"Parsed response: {content}")

    return {
        "type": content["type"],
        "tool": content.get("tool"),
        "args": content.get("args"),
        "message": content.get("response"),
    }
