from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from src.tools.get_distinct_values import get_distinct_values
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

model = init_chat_model("gemini-3.1-flash-lite", 
                        model_provider="google_genai")

class StructuredValidation(BaseModel):
    is_valid: bool = Field(
        description="True si la requête SQL répond EXACTEMENT à la demande utilisateur, False sinon."
    )
    explanation: str = Field(
        description="Si la requête est invalide, explique clairement pourquoi la logique métier n'est pas bonne."
    )


system_prompt = """Tu es un auditeur et expert SQL senior. Ton rôle est de valider la pertinence d'une requête SQL.

RÈGLES DE VALIDATION STRICTES :
1. **Fidélité au besoin** : La requête doit répondre STRICTEMENT à la question posée.
2. **Logique des jointures & Doublons dans les agrégations (ATTENTION CRITIQUE)** :
   - Fais très attention aux fonctions d'agrégation (`AVG`, `SUM`, `COUNT`) combinées avec des `JOIN`.
   - Si une table A est jointe à une table B (ex: `employes` JOIN `projets`) et qu'une fonction d'agrégation comme `AVG(e.salaire)` est appliquée directement sur le résultat du JOIN, la jointure duplique les lignes et fausse le calcul si un employé gère plusieurs projets.
   - Dans ce cas, tu DOIS déclarer la requête invalide (`is_valid = False`) et exiger l'utilisation d'une sous-requête `WHERE id IN (SELECT DISTINCT ...)` pour éliminer les doublons.
3. **Filtres et conditions** : Vérifie que les clauses WHERE, GROUP BY et HAVING correspondent aux critères demandés.

Si la requête comporte la moindre erreur logique, un risque de doublon d'agrégation ou ne répond pas exactement au besoin, définis `is_valid` à False et détaille la correction dans `explanation`."""
    

agent_validator = create_agent(
    model=model,
    tools=[get_distinct_values],
    system_prompt=system_prompt,
    response_format=ToolStrategy(StructuredValidation)
)