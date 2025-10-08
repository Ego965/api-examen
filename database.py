from pymongo import MongoClient
from pymongo.database import Database
from typing import Generator

# Usaremos la URI local estándar 27015
MONGO_URI = "mongodb://localhost:27015/"
# Nombramos la base de datos de manera más genérica para el examen
DB_NAME = "examen_api" 

def get_db() -> Generator[Database, None, None]:
    """
    Dependencia de FastAPI para obtener una conexión a MongoDB.
    
    Abre y cierra la conexión automáticamente gracias al patrón 'yield'.
    """
    client = MongoClient(MONGO_URI)
    try:
        # Retorna la base de datos específica.
        db = client[DB_NAME]
        yield db
    finally:
        # Asegura que la conexión se cierre al finalizar la solicitud.
        client.close()