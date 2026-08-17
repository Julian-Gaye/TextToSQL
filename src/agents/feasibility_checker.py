from typing import Literal
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from src.tools.get_distinct_values import get_distinct_values
from langchain.agents.structured_output import ToolStrategy

model = init_chat_model("gemini-3.1-flash-lite", 
                        model_provider="google_genai")

class StructuredRelevance(BaseModel):
    category: Literal["general_conversation", "impossible_sql", "feasible_sql"] = Field(
        description="La catégorie de la demande."
    )
    reason: str = Field(
        description="Si la catégorie est 'impossible_sql', explique pourquoi.",
        default=""
    )

system_prompt = f"""Analyse la demande de l'utilisateur par rapport au schéma de la base de données.
Tu peux utiliser les tools à ta disposition pour avoir plus d'information.
Classifie la demande dans l'une de ces 3 catégories :
1. "general_conversation" : Toute question ne cherchant pas à extraire des données de la BDD (Salutations, question générale, etc).
2. "impossible_sql" : L'utilisateur VEUT extraire des données, mais les tables/colonnes demandées n'existent pas ou la logique est infaisable avec ce schéma.
3. "feasible_sql" : L'utilisateur veut extraire des données et la BDD contient ce qu'il faut.
"""

agent_relevance_checker = create_agent(
    model=model,
    tools=[get_distinct_values],
    system_prompt=system_prompt,
    response_format=ToolStrategy(StructuredRelevance)
)