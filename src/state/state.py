from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

class SqlState(TypedDict):
    user_request: str
    messages: Annotated[list[AnyMessage], add_messages]
    generated_sql: str
    syntax_error: str
    attempts: int
    is_valid: bool
    feedback: str
    result: list