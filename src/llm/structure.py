EXECUTOR_OUTPUT_STRUCTUR = {
  "type": "json_object",
  "properties": {
    "type": {
      "type": "string",
      "enum": [
        "tool_call",
        "step_result"
      ]
    },

    "tool": {
      "type": ["string", "null"]
    },

    "args": {
      "type": ["object", "null"]
    },

    "status": {
      "type": [
        "string",
        "null"
      ],
      "enum": [
        "completed",
        "failed",
        "needs_user_input",
        "in_progress",
        "null"
      ]
    },

    "summary": {
      "type": [
        "string",
        "null"
      ]
    },

    "artifacts": {
      "type": [
        "object",
        "null"
      ]
    },

    "user_question": {
      "type": [
        "string",
        "null"
      ]
    }
  },

  "required": [
    "type",
    "tool",
    "args",
    "status",
    "summary",
    "artifacts",
    "user_question"
  ],

  "additionalProperties": False
}
PLANNER_OUTPUT_STRUCTURE = {
    "type": "json_object",
    "properties": {
        "goal": {
            "type": "string",
            "description": "Overall objective of the user's request."
        },
        "summary": {
            "type": "string",
            "description": "A brief summary of the planning process and results."
        },
        "steps": {
            "type": "array",
            "description": "Ordered high-level tasks required to accomplish the goal.",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "description": {
                        "type": "string",
                        "description": "A high-level description of the task."
                    },
                    "expected_output": {
                        "type": "string",
                        "description": "What successful completion of this step should produce."
                    },
                    "depends_on": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        },
                        "description": "IDs of prerequisite steps."
                    }
                },
                "required": [
                    "id",
                    "description",
                    "expected_output",
                    "depends_on",
                ]
            }
        }
    },
    "required": [
        "goal",
        "summary",
        "steps"
    ]
}

AGENT_OUTPUT_STRUCTURE = {
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

SUMMERIZER_STRUCTURE = {
    "type": "json_schema",
    "json_schema": {
        "name": "conversation_summary",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "A concise summary of the conversation",
                },
                "facts": {
                    "type": "array",
                    "description": "Important facts extracted from the conversation",
                    "items": {"type": "string"},
                },
                "open_tasks": {
                    "type": "array",
                    "description": "Tasks the user has not finished yet",
                    "items": {"type": "string"},
                },
                "last_summarized_index": {
                    "type": "integer",
                    "description": "Index of the last conversation message included in this summary",
                },
            },
            "required": ["summary", "facts", "last_summarized_index"],
            "additionalProperties": False,
        },
    },
}
