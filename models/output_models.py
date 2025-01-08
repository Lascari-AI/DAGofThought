from pydantic import BaseModel, Field
from typing import List, Union, Literal, Type
from enum import Enum


class AtomicStep(BaseModel):
    key: str = Field(
        ...,
        description="Key of the atomic step. Must have format of AS_<number> (ex: AS_1, AS_2, etc.)",
    )
    previous_step_key: Union[str, Literal["None"]] = Field(
        ...,
        description="Key of the previous atomic step (ex: AS_1, AS_2, etc.). If this is the first step, must be the literal string 'None'.",
    )
    content: Union[str, Literal["DEAD_END"]] = Field(
        ...,
        description="Use short, simple sentences that mirror natural thought patterns",
    )


class FoundationObservation(BaseModel):
    key: str = Field(
        ...,
        description="Key of the foundation observation. Must have format of FO_<number> (ex: FO_1, FO_2, etc.)",
    )
    name: str = Field(..., description="General name of the foundation observation.")
    atomic_steps: List[AtomicStep] = Field(
        ...,
        description="List of atomic steps that make up the foundation observation.",
    )


class Thought(BaseModel):
    key: str = Field(
        ...,
        description="Key of the thought. Must have format of TH_<number> (ex: TH_1, TH_2, etc.)",
    )
    backtracked_from: Union[str, Literal["None"]] = Field(
        ...,
        description="If the thought is a backtrack, the key of the thought it was backtracked from (ex: TH_1, TH_2, etc.). If not, must be the literal string 'None'.",
    )
    parent_thought: Union[str, Literal["None"]] = Field(
        ...,
        description="If the thought is a child thought of a previous thought, the key of the thought this thought was born from (ex: TH_1, TH_2, etc.). If not, must be the literal string 'None'.",
    )
    associated_foundation_observations: List[str] = Field(
        ...,
        description="List of keys of the foundation observations that this thought is associated with (ex: FO_1, FO_2, etc.).",
    )
    name: str = Field(
        ...,
        description="Use short, simple sentences that mirror natural thought patterns",
    )
    guard_rails_to_consider: List["GuardRailEnum"] = Field(
        ..., description="Guard rails to consider at this step."
    )
    thought_process: List[AtomicStep] = Field(
        ..., description="List of atomic steps that make up the thought."
    )


class ReasoningProcess(BaseModel):
    foundation_observations: List[FoundationObservation] = Field(
        ...,
        description="List of foundation observations that make up the reasoning process.",
    )
    thoughts: List[Thought] = Field(
        ..., description="List of thoughts that make up the reasoning process."
    )


class InDepthStructuredReasoning(BaseModel):
    reasoning_process: ReasoningProcess = Field(
        ...,
        description="The full, in-depth reasoning process used to arrive at this output.",
    )
    findings_summary: str = Field(
        ..., description="An in depth summary of your findings."
    )
    remaining_questions: List[str] = Field(
        ...,
        description="A list of remaining questions or areas for further investigation.",
    )
    is_conclusion_premature: bool = Field(
        ..., description="Whether the conclusion is premature or not."
    )
    reason_for_premature_conclusion: Literal["conclusion NOT premature"] | str = Field(
        ...,
        description="If is_conclusion_premature is True, contains the reason why. If False, must be the literal string 'conclusion NOT premature'.",
    )


def get_classes_with_enum(guardRailEnum: Enum) -> Type[InDepthStructuredReasoning]:
    """Helper function that allows dynamic configuration of guard rail enums.

    This function takes a user-defined enum class for guard rails and updates the
    Thought model's guard_rails_to_consider field to use that enum type. This ensures
    the guard rails are stored as enum keys rather than full enum objects, while
    allowing the guard rail options to be defined at runtime.

    Args:
        guardRailEnum: The enum class containing the allowed guard rail values

    Returns:
        The InDepthStructuredReasoning model class with updated guard rail typing
    """
    Thought.model_fields["guard_rails_to_consider"].annotation = List[guardRailEnum]
    return InDepthStructuredReasoning
