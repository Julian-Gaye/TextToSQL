from langchain.agents import create_agent
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from src.tools.get_schema import get_schema
from src.tools.get_distinct_values import get_distinct_values
from langchain.agents.structured_output import ToolStrategy

model = init_chat_model("gemini-3.1-flash-lite", 
                        model_provider="google_genai")

class StructuredGeneration(BaseModel):
    generated_sql: str = Field(
        description="La requête SQL SELECT générée sans explications autour."
    )

system_prompt = f"""Tu es un assistant expert en SQL. 
Ta mission est de générer une requête SQL valide pour répondre à la question posée par l'utilisateur.
- Génère uniquement des requêtes SELECT.
- Si un message t'indique une erreur de syntaxe ou de logique sur ta proposition précédente, analyse l'erreur et génère une requête SQL corrigée."""

agent_generator = create_agent(
    model=model,
    tools=[get_schema, get_distinct_values],
    system_prompt=system_prompt,
    response_format=ToolStrategy(StructuredGeneration)
)