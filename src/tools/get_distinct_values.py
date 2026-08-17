from database.database import db_conn
from langchain_core.tools import tool

@tool
def get_distinct_values(table_name: str, column_name: str) -> str:
    """
    Retourne les valeurs uniques (limitées à 10) d'une colonne texte.
    Utile pour connaître la casse ou l'orthographe exacte des catégories avant un WHERE.
    """
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT DISTINCT {column_name} FROM {table_name} LIMIT 10;")
    values = cursor.fetchall()
    
    values_info = []
    for value in values:
        value = value[0]
        values_info.append(f"{value}")
        
    return "\n".join(values_info)