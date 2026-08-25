import sys
from dotenv import load_dotenv
from tabulate import tabulate
from src.graph.graph import create_builder
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

load_dotenv()

def get_user_input(interrupt_info):
    question = interrupt_info.get("question", str(interrupt_info))
    user_choice = input(f"\n{question}\n(oui/non) : ").strip().lower()
    return user_choice in ["o", "oui", "y", "yes"]

def run_graph(user_request: str):
    state = {
        "user_request": user_request,
    }

    print(f"\n\n======== Requête ========")
    print(f"Question : {user_request}")

    checkpointer = InMemorySaver()
    builder = create_builder()
    graph = builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "thread-1"}}
    
    while True:
        graph.invoke(state, config=config)

        state_snapshot = graph.get_state(config)

        if not state_snapshot.next:
            result = state_snapshot.values
            break

        interrupt_info = state_snapshot.tasks[0].interrupts[0].value
        user_response = get_user_input(interrupt_info)
        state = Command(resume=user_response)
    
    if result.get("status") == "success":
        print("\n======== Résultat ========")
        print(f"Requête SQL : {result.get('generated_sql')}")
        print(tabulate(result.get('result', []), headers="keys", tablefmt="psql"))
    else:
        print(f"\n======== Requête ({result.get('status', 'refused')}) ========")
        print(result.get("reason", "Requête annulée."))



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
        run_graph("Quel est le salaire moyen des chefs de projet ?")