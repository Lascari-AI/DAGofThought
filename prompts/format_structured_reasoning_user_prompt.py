import json
from typing import List
from models.input_models import GuardRail


def format_structured_reasoning_user_prompt(
    task: str, guardrails: List[GuardRail] = []
) -> str:
    output = f""" Please provide a detailed step by step reasoning process for the following task:
# Task: 
{task}
"""
    if len(guardrails) > 0:
        output += "\n# Guardrails:\n" + "\n".join(
            json.dumps(g.model_dump(), indent=2) for g in guardrails
        )

    return output
