import json
from pathlib import Path


def append_to_converstaion(data, conversation_id):
    """
    Write JSON data to a file.

    Args:
        data (dict): The JSON data to write.
        conversation_id (str): The ID of the conversation.
    """
    if not data:
        return
    file_path = Path(f"data/conversations/{conversation_id}.json")
    # Ensure the directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_conversation_messages(conversation_id):
    """
    Retrieve conversation memory from a JSON file.

    Args:
        conversation_id (str): The ID of the conversation.
    Returns:
        dict: The conversation memory if the file exists, otherwise an empty dictionary.
    """
    file_path = Path(f"data/conversations/{conversation_id}.json")
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}
