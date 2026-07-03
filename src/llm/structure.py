AGENT_OUTPUT_STRUCTURE ={
                            "type": "json_schema",
                            "json_schema": {
                                "name": "assisstant response",
                                "strict": True,
                                "schema": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                    "type": "string",
                                    "description": "final or tool_call, if final this is your final answer and you do not need any tools, so tool and args should be empty",
                                    },
                                    "tool": {
                                    "type": "string",
                                    "description": "tool name if type is tool_call",
                                    },
                                    "args": {
                                    "type": "string",
                                    "description": "args for the tool if type is tool_call",
                                    },                                
                                    "response": {
                                    "type": "string",
                                    "description": "llm response",
                                    },
                                },
                                "required": ["type", "response"],
                                "additionalProperties": False,
                                },
                            },
                        }

SUMMERIZER_STRUCTURE  = {
    "type": "json_schema",
    "json_schema": {
        "name": "conversation_summary",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "A concise summary of the conversation"
                },
                "facts": {
                    "type": "array",
                    "description": "Important facts extracted from the conversation",
                    "items": {
                        "type": "string"
                    }
                },
                "open_tasks": {
                    "type": "array",
                    "description": "Tasks the user has not finished yet",
                    "items": {
                        "type": "string"
                    }
            },
                "last_summarized_index": {
                    "type": "integer",
                    "description": "Index of the last conversation message included in this summary"
                }

            },
            "required": [
                "summary",
                "facts",
                "last_summarized_index"
            ],
            "additionalProperties": False
        }
    }
}