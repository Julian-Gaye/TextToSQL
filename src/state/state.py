from typing import TypedDict, Literal

class InputState(TypedDict):
    user_request: str

class OutputState(TypedDict):
    status: Literal["success", "refused", "error"]
    generated_sql: str
    result: list
    reason: str

class OverallState(TypedDict):
    status: Literal["success", "refused", "error"]
    user_request: str
    schema: str
    generated_sql: str
    syntax_error: str
    attempts: int
    is_valid: bool
    feedback: str
    result: list
    category: Literal["general_conversation", "impossible_sql", "feasible_sql"]
    reason: str