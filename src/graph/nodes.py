from src.agents.feasibility_checker import StructuredRelevance
from src.agents.feasibility_checker import agent_relevance_checker
from src.agents.generator import StructuredGeneration
from src.agents.validator import StructuredValidation
from src.agents.generator import agent_generator
from src.agents.validator import agent_validator
from database.database import db_conn
from src.state.state import InputState, OutputState, OverallState

def node_get_schema(state: InputState) -> OverallState:
    cursor = db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = []
    for table_name in tables:
        name = table_name[0]
        cursor.execute(f"PRAGMA table_info({name});")
        columns = cursor.fetchall()
        cols_desc = ", ".join([f"{col[1]} ({col[2]})" for col in columns])
        schema_info.append(f"Table '{name}' -> Colonnes : [{cols_desc}]")
        
    return {
        "schema": "\n".join(schema_info)
    }

def node_agent_check_relevance(state: OverallState) -> OverallState:
    schema = state.get("schema")
    user_request = state.get("user_request")

    messages = [("system", f"Voici le schéma de la BDD :\n{schema}")]
    messages.append(("user", user_request))
    
    response: StructuredRelevance = agent_relevance_checker.invoke({
            "messages": messages
    })

    structured_response = response.get("structured_response")
    
    category = ""
    reason = ""

    if structured_response:
        category = structured_response.category
        reason = structured_response.reason
    
    return {
        "category": category,
        "reason": reason
    }

def node_agent_generator(state: OverallState) -> OverallState:
    schema = state["schema"]
    user_request = state["user_request"]
    syntax_error = state.get("syntax_error")
    feedback = state.get("feedback")
    previous_sql = state.get("generated_sql")

    messages = [("system", f"Voici le schéma de la BDD :\n{schema}")]

    if syntax_error:
        messages.append((
            "system",
            f"LA SYNTAXE DE LA REQUETE SQL PRECEDENTE EST INCORRECTE :\n"
            f"- Requête : `{previous_sql}`\n"
            f"- Erreur SQL : {syntax_error}\n"
            f"Consigne : Corrige la requête sql pour résoudre cette erreur."
        ))
    elif feedback:
        messages.append((
            "system",
            f"LA TENTATIVE PRECEDENTE NE REPOND PAS EXACTEMENT A LA DEMANDE DE L'UTILISATEUR :\n"
            f"- Requête : `{previous_sql}`\n"
            f"- Remarque du validateur : {feedback}\n"
            f"Consigne : Ajuste la requête sql pour prendre en compte ces remarques."
        ))

    messages.append(("user", user_request))

    response: StructuredGeneration = agent_generator.invoke({"messages": messages})
    structured_response = response.get("structured_response")

    generated_sql = ""
    if structured_response:
        generated_sql = structured_response.generated_sql

    return {
        "generated_sql": generated_sql,
        "attempts": state.get("attempts", 0) + 1,
        "syntax_error": "",
        "feedback": ""
    }

def node_check_syntax(state: OverallState) -> OverallState:
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

def node_agent_validator(state: OverallState) -> OverallState:
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

def node_execute_sql(state: OverallState) -> OutputState:
    cursor = db_conn.cursor()
    cursor.execute(state["generated_sql"])
    results = cursor.fetchall()
    return {
        "generated_sql": state["generated_sql"],
        "result": results
    }

def node_general_conversation(state: OverallState) -> OutputState:
    return {
        "reason": "Ceci n'est pas une requête SQL"
    }

def node_impossible_sql(state: OverallState) -> OutputState:
    pass