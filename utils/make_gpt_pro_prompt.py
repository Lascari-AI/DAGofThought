import json
from typing import List
from enum import Enum
from models.input_models import GuardRail
from instructor.function_calls import openai_schema
from models.output_models import get_classes_with_enum
from prompts.format_structured_reasoning_user_prompt import (
    format_structured_reasoning_user_prompt,
)


def make_gpt_pro_prompt(
    IN_DEPTH_THINKING_SYSTEM_PROMPT: str,
    task: str,
    guardrails: List[GuardRail] = [],
    guardrail_enum: Enum = None,
):
    output = ""
    output += "<system prompt>\n"
    output += IN_DEPTH_THINKING_SYSTEM_PROMPT

    output += "\n\n # Response Model\n"
    output += "You must respond with a valid JSON object that matches the response model below:\n"
    output += "<response model>\n"
    output += json.dumps(
        openai_schema(get_classes_with_enum(guardrail_enum)).openai_schema, indent=2
    )
    output += "\n</response model>\n"
    output += "\n</system prompt>\n\n\n"
    output += "<user prompt>\n"
    output += format_structured_reasoning_user_prompt(task, guardrails)
    output += "\n</user prompt>\n"

    return output
