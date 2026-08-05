from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from src.graph.workflow import workflow

load_dotenv()

def run_graph(user_request: str):
    state = {
        "user_request": user_request,
        "messages": [HumanMessage(content=user_request)]
    }

    result = workflow.invoke(state)
    print("======== Résultat ========")
    print(f"Requête SQL : {result.get("generated_sql")}")
    print(f"Résultats : {result.get("result")}")


if __name__ == "__main__":
    run_graph("Donne moi la liste des personnes qui travaillent dans la tech")