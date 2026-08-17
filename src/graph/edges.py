from langgraph.constants import END
from typing import Literal
from src.state.state import OverallState

def edge_syntax(state: OverallState) -> Literal["agent_generator", "agent_validator", END]:
    if state.get("syntax_error"):
        if state.get("attempts", 0) >= 3:
            return END
        return "agent_generator"
    return "agent_validator"

def edge_validation(state: OverallState) -> Literal["agent_generator", "execute_sql", END]:
    if not state.get("is_valid"):
        if state.get("attempts", 0) >= 3:
            return END
        return "agent_generator"
    return "execute_sql"

def edge_relevance(state: OverallState) -> Literal["agent_generator", "general_conversation", "impossible_sql"]:
    if state.get("category") == "general_conversation":
        return "general_conversation"
    elif state.get("category") == "impossible_sql":
        return "impossible_sql"
    return "agent_generator"