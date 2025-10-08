from fastapi import FastAPI, Depends, HTTPException, Path, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# IMPORTANTE: Importar las nuevas funciones y modelos del archivo estudiante.py
from database import get_db
from estudiante import (
    EstudianteCreate,
    EstudianteResponse,
    create_estudiante,
    get_all_estudiantes,
    get_estudiante_by_id,
    update_estudiante,
    delete_estudiante,
    create_many_estudiantes 
)

app = FastAPI(
    title="API de Estudiantes (Examen Práctico)",
    description="Implementación completa de API CRUD con FastAPI y MongoDB."
)

# CORS Middleware (se mantiene)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Endpoints CRUD de Estudiantes (10 Puntos) ---

ESTUDIANTE_TAG = "Estudiantes"
ID_PATH = Path(
    ...,
    title="ID del Estudiante",
    min_length=24,
    max_length=24,
    regex="^[0-9a-fA-F]{24}$",
    description="Debe ser un ObjectId de 24 caracteres hexadecimales."
)


# 1. Método GET – lista de estudiantes (2 puntos)
@app.get("/estudiantes", response_model=List[EstudianteResponse], tags=[ESTUDIANTE_TAG])
def get_all_estudiantes_api(db=Depends(get_db)):
    """Obtiene la lista completa de todos los estudiantes."""
    try:
        return get_all_estudiantes(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la lista de estudiantes: {e}")


# 2. Método GET <id> - estudiante por id (2 puntos)
@app.get("/estudiantes/{estudiante_id}", response_model=EstudianteResponse, tags=[ESTUDIANTE_TAG])
def get_one_estudiante_api(
    estudiante_id: str = ID_PATH,
    db=Depends(get_db)
):
    """Obtiene un estudiante específico usando su ID."""
    try:
        estudiante = get_estudiante_by_id(db, estudiante_id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado o ID inválido")
        return estudiante
    except HTTPException:
        raise # Re-lanza la HTTPException
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el estudiante: {e}")


# 3. Método POST – crear estudiante nuevo (2 puntos)
@app.post("/estudiantes", response_model=EstudianteResponse, status_code=201, tags=[ESTUDIANTE_TAG])
def create_one_estudiante_api(estudiante: EstudianteCreate, db=Depends(get_db)):
    """Crea un nuevo registro de estudiante."""
    try:
        return create_estudiante(db, estudiante)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el estudiante: {e}")


# 4. Método PUT <id> - actualizar estudiante (2 puntos)
# AHORA CORRECTO
@app.put("/estudiantes/{estudiante_id}", response_model=EstudianteResponse, tags=[ESTUDIANTE_TAG])
def update_one_estudiante_api(
    # 1. Parámetro sin valor por defecto (el cuerpo de la solicitud)
    estudiante_data: EstudianteCreate, 
    
    # 2. Parámetros con valor por defecto (FastAPI Dependencies)
    estudiante_id: str = ID_PATH,
    db=Depends(get_db)
):
    """Actualiza completamente un estudiante existente usando su ID."""
    try:
        updated_estudiante = update_estudiante(db, estudiante_id, estudiante_data)
        if not updated_estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado o ID inválido")
        return updated_estudiante
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el estudiante: {e}")


# 5. Método DELETE <id> – eliminar estudiante (2 puntos)
@app.delete("/estudiantes/{estudiante_id}", status_code=204, tags=[ESTUDIANTE_TAG])
def delete_one_estudiante_api(
    estudiante_id: str = ID_PATH,
    db=Depends(get_db)
):
    """Elimina un estudiante usando su ID. Retorna 204 No Content si es exitoso."""
    try:
        if not delete_estudiante(db, estudiante_id):
            raise HTTPException(status_code=404, detail="Estudiante no encontrado o ID inválido")
        # Retorna una respuesta vacía con código 204
        return Response(status_code=204) 
    except HTTPException:
        raise # Re-lanza la HTTPException
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el estudiante: {e}")


# --- Endpoint de Prueba (Root) ---

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint de prueba de funcionamiento."""
    return {"message": "Bienvenido a la API de Estudiantes con FastAPI"}

# --- Nuevo Endpoint para Crear Múltiples Estudiantes ---

@app.post("/estudiantes/bulk", response_model=List[EstudianteResponse], status_code=201, tags=[ESTUDIANTE_TAG])
def create_many_estudiantes_api(estudiantes: List[EstudianteCreate], db=Depends(get_db)):
    """
    Crea múltiples registros de estudiantes en una sola solicitud.
    
    El cuerpo de la solicitud debe ser un array JSON.
    """
    if not estudiantes:
        raise HTTPException(status_code=400, detail="La lista de estudiantes no puede estar vacía.")

    try:
        new_estudiantes = create_many_estudiantes(db, estudiantes)
        return new_estudiantes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear múltiples estudiantes: {e}")