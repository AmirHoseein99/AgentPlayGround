from ..logger import get_logger


def agent_format_response(response):
    parser_logger = get_logger("agent_parser")

    try:
        if "choices" not in response or len(response["choices"]) == 0:
            parser_logger.error(f"Invalid OpenRouter response: {response}")
            raise ValueError("Invalid OpenRouter response")

        content = response["choices"][0]["message"]["content"]

        parser_logger.info(f"Received model response: {content}")

        return content

    except Exception as e:
        parser_logger.exception(f"Failed to parse OpenRouter response: {e}")
        raise
