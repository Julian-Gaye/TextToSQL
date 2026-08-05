from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from src.tools.get_distinct_values import get_distinct_values
from src.tools.get_schema import get_schema
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
        RÈGLES DE VALIDATION :\n
        1. **Fidélité au besoin** : La requête doit répondre STRICTEMENT à la question posée, sans en faire trop ni pas assez.\n
        2. **Logique des jointures** : Vérifie que les JOIN utilisés sont corrects et ne créent pas de doublons ou de cartésiens involontaires.\n
        3. **Filtres et conditions** : Vérifie que les clauses WHERE, GROUP BY et HAVING correspondent aux critères demandés.\n
        4. **Sécurité & Cohérence** : Seules les requêtes de lecture (SELECT) sont autorisées.\n\n
        Si la requête comporte la moindre erreur logique ou ne répond pas exactement au besoin, 
        définis `is_valid` à False et détaille précisément la correction attendue dans `explanation`."""
    

agent_validator = create_agent(
    model=model,
    tools=[get_schema, get_distinct_values],
    system_prompt=system_prompt,
    response_format=ToolStrategy(StructuredValidation)
)