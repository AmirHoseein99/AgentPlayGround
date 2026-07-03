from pathlib import Path
import json
import os


def append_to_conversation(role, content, conversation_id, tool_name=None):

    file_path = Path(f"data/conversations/{conversation_id}/{conversation_id}.json")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # load
    if file_path.exists():
        try:
            payload = json.loads(file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = []
    else:
        payload = []

    entry = {"role": role, "content": content}

    if tool_name:
        entry["tool_name"] = tool_name

    payload.append(entry)

    # atomic write
    tmp_path = file_path.with_suffix(".tmp")

    tmp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=4), encoding="utf-8"
    )

    os.replace(tmp_path, file_path)


def get_conversation_messages(conversation_id):
    """
    Retrieve conversation memory from a JSON file.

    Args:
        conversation_id (str): The ID of the conversation.
    Returns:
        list: The conversation memory if the file exists, otherwise an empty dictionary.
    """
    file_path = Path(f"data/conversations/{conversation_id}/{conversation_id}.json")

    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        normalized = []

        for m in data:
            normalized.append(
                {
                    "role": m["role"],
                    "content": (
                        m["content"]
                        if isinstance(m["content"], str)
                        else json.dumps(m["content"])
                    ),
                }
            )

        return normalized

    except Exception:
        return []
