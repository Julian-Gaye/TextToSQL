from langchain_core.messages import AIMessage
from src.agents.generator import StructuredGeneration
from src.agents.validator import StructuredValidation
from src.agents.generator import agent_generator
from src.agents.validator import agent_validator
from database.database import db_conn
from src.state.state import SqlState

def node_agent_generator(state: SqlState):
    print("Agent Générateur")
    response: StructuredGeneration = agent_generator.invoke({"messages": state["messages"]})

    structured_response = response.get("structured_response")

    generated_sql = ""
    if structured_response:
        generated_sql = structured_response.generated_sql

    return {
        "messages": [AIMessage(content=generated_sql)],
        "generated_sql": generated_sql,
        "attempts": state.get("attempts", 0) + 1
    }

def node_check_syntax(state: SqlState):
    print("Vérification syntaxique")
    sql = state.get("generated_sql")
    
    if not sql:
        return {"syntax_error": "Aucune requête SQL SELECT n'a été détectée."}

    if any(key in sql.upper() for key in ["DELETE", "DROP", "UPDATE", "INSERT"]):
        return {"syntax_error": "Opération interdite (Seul SELECT est autorisé)"}
        
    cursor = db_conn.cursor()
    try:
        cursor.execute(f"EXPLAIN QUERY PLAN {sql}")
        return {"syntax_error": ""}
    except Exception as e:
        return {"syntax_error": str(e)}

def node_agent_validator(state: SqlState):
    print("Agent Validateur")
    user_request = state.get("user_request")
    generated_sql = state.get("generated_sql")

    input_prompt = (
        f"Question utilisateur : {user_request}\n"
        f"Requête SQL à évaluer : {generated_sql}"
    )
    
    response: StructuredValidation = agent_validator.invoke({
        "messages": [("user", input_prompt)]
    })

    structured_response = response.get("structured_response")
    
    is_valid = False
    feedback = ""

    if structured_response:
        is_valid = structured_response.is_valid
        feedback = structured_response.explanation
    
    return {
        "is_valid": is_valid,
        "feedback": feedback
    }

def node_execute_sql(state: SqlState):
    print("Exécution requête")
    cursor = db_conn.cursor()
    cursor.execute(state["generated_sql"])
    results = cursor.fetchall()
    return {
        "generated_sql": state["generated_sql"],
        "result": results
    }