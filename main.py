import sys
from dotenv import load_dotenv
from src.graph.workflow import workflow

load_dotenv()

def run_graph(user_request: str):
    state = {
        "user_request": user_request,
    }

    print(f"\n\n======== Requête ========")
    print(f"Question : {user_request}")

    result = workflow.invoke(state)
    
    if result.get("generated_sql") is not None:
        print("======== Résultat ========")
        print(f"Requête SQL : {result.get("generated_sql")}")
        print(f"Résultats : {result.get("result")}")
    else:
        print("======== Requête refusée ========")
        print(result.get("reason"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1] 
        run_graph(query)
    else:
        run_graph("Salut ! comment ça va ?")
        run_graph("Donne moi la liste des employés qui ont une voiture")
        run_graph("Donne moi la liste des employés")
        run_graph("Qui sont les employés qui travaillent dans la tech ?")
        run_graph("Qui sont les employés qui travaillent dans l'IT?")
        run_graph("Supprimer la table employes")
