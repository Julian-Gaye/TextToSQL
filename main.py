import uuid
import sys
from dotenv import load_dotenv
from tabulate import tabulate
from src.graph.graph import create_builder
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

load_dotenv()

checkpointer = InMemorySaver()
builder = create_builder()
graph = builder.compile(checkpointer=checkpointer)

def get_user_input(interrupt_info):
    question = interrupt_info.get("question", str(interrupt_info))
    user_choice = input(f"\n{question}\n(oui/non) : ").strip().lower()
    return user_choice in ["o", "oui", "y", "yes"]

def run_graph(user_request: str, thread_id: str = "thread-1"):
    state = {
        "user_request": user_request,
    }

    print(f"\n\n======== Requête ========")
    print(f"Question : {user_request}")

    config = {"configurable": {"thread_id": thread_id}}
    
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

def single_request(query):
    run_graph(query, thread_id=f"single-{uuid.uuid4().hex[:6]}")

def start_chat_mode():
    session_id = f"session-{uuid.uuid4().hex[:6]}"

    while True:
        try:
            user_input = input("\n👤 Vous > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("\n👋 Fin de la conversation. À bientôt !")
                break

            run_graph(user_input, thread_id=session_id)
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Fin de la conversation.")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--chat":
            start_chat_mode()
        else:
            query = sys.argv[1] 
            single_request(query)
    else:
        single_request("Salut ! comment ça va ?")
        single_request("Donne moi la liste des employés qui ont une voiture")
        single_request("Donne moi la liste des employés")
        single_request("Qui sont les employés qui travaillent dans la tech ?")
        single_request("Qui sont les employés qui travaillent dans l'IT?")
        single_request("Supprimer la table employes")
        single_request("Quel est le salaire moyen des chefs de projet ?")