from memory.memory_manager import (
    initialize_conversation,
    remove_conversation,
    append_to_conversation,
    load_conversation,
    summarize_conversation,
    load_memory,
    get_context,
)

def test_memory_flow(conversation_id='test'):

    remove_conversation(conversation_id)
    initialize_conversation(conversation_id)

    messages = [
        ("user", "Hi! I am building an AI agent framework in Python."),
        ("assistant", "That sounds interesting."),
        ("user", "I am using OpenRouter."),
        ("assistant", "Good choice."),
        ("user", "I implemented structured outputs."),
        ("assistant", "Nice."),
        ("user", "Now I am working on memory."),
        ("assistant", "Good."),
    ]

    for role, content in messages:
        append_to_conversation(
            conversation_id=conversation_id,
            role=role,
            content=content
        )

    # --------------------------
    # ASSERT 1: messages stored
    # --------------------------
    conv = load_conversation(conversation_id)
    assert len(conv) == len(messages)

    # --------------------------
    # ACT: summarize
    # --------------------------
    summarize_conversation(conversation_id)

    # --------------------------
    # ASSERT 2: memory exists
    # --------------------------
    memory = load_memory(conversation_id)
    assert memory is not None

    # --------------------------
    # ASSERT 3: context returned
    # --------------------------
    context = get_context(conversation_id)
    assert isinstance(context, list)
    assert len(context) > 0

    # context should include structured messages
    roles = [m["role"] for m in context]
    assert "user" in roles
    assert "assistant" in roles