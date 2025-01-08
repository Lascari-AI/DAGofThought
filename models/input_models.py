from pydantic import BaseModel, Field


class GuardRail(BaseModel):
    name: str = Field(..., description="General name of the guard rail.")
    description: str = Field(
        ...,
        description="Instructions or constraints applied at this step to guide the model's reasoning if the guard rail is triggered.",
    )
