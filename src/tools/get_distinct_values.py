from database.database import db_conn
from langchain_core.tools import tool

@tool
def get_distinct_values(table_name: str, column_name: str) -> str:
    """
    Retourne les valeurs uniques d'une colonne texte.
    Utile pour connaître la casse ou l'orthographe exacte des catégories avant un WHERE.
    """
    cursor = db_conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    if not cursor.fetchone():
        return f"Erreur : La table '{table_name}' n'existe pas."

    cursor.execute(f'PRAGMA table_info("{table_name}");')
    valid_columns = [col[1] for col in cursor.fetchall()]
    if column_name not in valid_columns:
        return f"Erreur : La colonne '{column_name}' n'existe pas dans la table '{table_name}'."

    cursor.execute(f'SELECT DISTINCT "{column_name}" FROM "{table_name}";')
    values = cursor.fetchall()
    
    values_info = []
    for value in values:
        value = value[0]
        values_info.append(f"{value}")
        
    return "\n".join(values_info)