from src.state.state import SqlState

def edge_syntax(state: SqlState) -> str:
    if state.get("syntax_error"):
        print(f"❌ Erreur de syntaxe : {state['syntax_error']}")
        if state.get("attempts", 0) >= 3:
            return "END"
        return "agent_generator"
    return "agent_validator"

def edge_validation(state: SqlState) -> str:
    if not state.get("is_valid"):
        print(f"❌ Invalide selon le validateur: {state['feedback']}")
        if state.get("attempts", 0) >= 3:
            return "END"
        return "agent_generator"
    return "execute_sql"