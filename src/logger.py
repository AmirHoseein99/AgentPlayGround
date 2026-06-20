from pathlib import Path
import logging

LOG_FILES = {
    "cli": "logs/cli.log",
    "agent": "logs/agent/agent.log",
    "agent_api": "logs/agent/api.log",
    "agent_parser": "logs/agent/parser.log",
    "web_search_tool": "logs/agent/tools/web_search.log",
    "python_executor_tool": "logs/agent/tools/python_executor.log",
    "openrouter": "logs/llm/openrouter/openrouter.log",
    "llm_api": "logs/llm/api.log",
    "llm_chat_engine": "logs/llm/chat_engine.log",
    "llm_parser": "logs/llm/parser.log",
}


def get_logger(name: str):
    log_path = LOG_FILES[name]

    # create folders
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # IMPORTANT: prevent duplicate handlers
    if logger.handlers:
        return logger

    handler = logging.FileHandler(log_path)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # IMPORTANT: avoid double logging via root logger
    logger.propagate = False

    return logger
