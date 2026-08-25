from langchain_core.tools import tool
from database.database import db_conn

@tool
def get_schema() -> str:
    """
    Inspecte la base de données et retourne la liste des tables
    ainsi que la structure exacte des colonnes.
    A utiliser dès qu'il faut comprendre quelles tables et colonnes sont disponibles.
    """
    cursor = db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = []
    for table_name in tables:
        name = table_name[0]
        cursor.execute(f'PRAGMA table_info("{name}");')
        columns = cursor.fetchall()
        cols_desc = ", ".join([f"{col[1]} ({col[2]})" for col in columns])
        schema_info.append(f"Table '{name}' -> Colonnes : [{cols_desc}]")
        
    return "\n".join(schema_info)