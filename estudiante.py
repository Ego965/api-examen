from pydantic import BaseModel, Field, BeforeValidator
from pymongo.database import Database
from datetime import datetime
from bson import ObjectId
from typing import List, Optional, Annotated

# La corrección para manejar la serialización de ObjectId
PydanticObjectId = Annotated[str, BeforeValidator(str)]
ESTUDIANTE_COLLECTION = "estudiantes"

# --- Modelos de Datos ---

# Modelo Base para Crear/Actualizar (lo que el cliente envía)
class EstudianteCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    apellido: str = Field(..., min_length=1)
    aprobado: bool = Field(default=False)
    nota: float = Field(..., ge=0.0, le=10.0) # Nota entre 0 y 10.0

# Modelo de Respuesta (lo que el servidor envía, incluyendo el ID y la fecha)
class EstudianteResponse(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    nombre: str
    apellido: str
    aprobado: bool
    nota: float
    fecha: datetime # Usamos datetime para la fecha

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "6502d1f5e8a6d5b12c7f9a01",
                "nombre": "Juan",
                "apellido": "Pérez",
                "aprobado": True,
                "nota": 7.5,
                "fecha": "2024-09-01T00:00:00Z"
            }
        }

# --- Funciones CRUD (Capa de Servicio) ---

# 1. Método POST - Crear estudiante (2 puntos)
def create_estudiante(db: Database, estudiante_data: EstudianteCreate) -> EstudianteResponse:
    """Crea un nuevo registro de estudiante."""
    new_estudiante = estudiante_data.model_dump() # Convierte Pydantic a dict
    new_estudiante["fecha"] = datetime.now() # Agrega la fecha actual

    result = db[ESTUDIANTE_COLLECTION].insert_one(new_estudiante)
    created_doc = db[ESTUDIANTE_COLLECTION].find_one({"_id": result.inserted_id})
    
    return EstudianteResponse.model_validate(created_doc)

# 2. Método GET - Lista de estudiantes (2 puntos)
def get_all_estudiantes(db: Database) -> List[EstudianteResponse]:
    """Obtiene la lista completa de estudiantes."""
    estudiantes_data = list(db[ESTUDIANTE_COLLECTION].find())
    return [EstudianteResponse.model_validate(est) for est in estudiantes_data]

# 3. Método GET <id> - Estudiante por ID (2 puntos)
def get_estudiante_by_id(db: Database, estudiante_id: str) -> Optional[EstudianteResponse]:
    """Obtiene un estudiante específico por su ObjectId."""
    if not ObjectId.is_valid(estudiante_id):
        return None
        
    doc = db[ESTUDIANTE_COLLECTION].find_one({"_id": ObjectId(estudiante_id)})
    
    if doc:
        return EstudianteResponse.model_validate(doc)
    return None

# 4. Método PUT <id> - Actualizar estudiante (2 puntos)
def update_estudiante(db: Database, estudiante_id: str, data: EstudianteCreate) -> Optional[EstudianteResponse]:
    """Actualiza completamente un estudiante existente."""
    if not ObjectId.is_valid(estudiante_id):
        return None

    # Obtenemos los datos, excluimos campos que no queremos actualizar (ej. el ID)
    updated_data = data.model_dump() 

    result = db[ESTUDIANTE_COLLECTION].update_one(
        {"_id": ObjectId(estudiante_id)}, 
        {"$set": updated_data}
    )
    
    if result.matched_count == 0:
        return None
        
    # Retornar el documento actualizado
    return get_estudiante_by_id(db, estudiante_id)

# 5. Método DELETE <id> - Eliminar estudiante (2 puntos)
def delete_estudiante(db: Database, estudiante_id: str) -> bool:
    """Elimina un estudiante por su ObjectId."""
    if not ObjectId.is_valid(estudiante_id):
        return False
        
    result = db[ESTUDIANTE_COLLECTION].delete_one({"_id": ObjectId(estudiante_id)})
    
    return result.deleted_count == 1


# ... (otras funciones CRUD) ...

def create_many_estudiantes(db: Database, estudiantes_data: List[EstudianteCreate]) -> List[EstudianteResponse]:
    """Crea múltiples registros de estudiantes en una sola operación de base de datos."""
    
    # 1. Preparar los datos para MongoDB
    documents_to_insert = []
    for estudiante in estudiantes_data:
        new_estudiante = estudiante.model_dump()
        new_estudiante["fecha"] = datetime.now() 
        documents_to_insert.append(new_estudiante)
        
    if not documents_to_insert:
        return []

    # 2. Insertar múltiples documentos de forma eficiente
    result = db[ESTUDIANTE_COLLECTION].insert_many(documents_to_insert)
    
    # 3. Recuperar y validar los documentos creados
    # Usamos los IDs generados por MongoDB para obtener los documentos
    created_docs = db[ESTUDIANTE_COLLECTION].find({"_id": {"$in": result.inserted_ids}})
    
    return [EstudianteResponse.model_validate(doc) for doc in created_docs]