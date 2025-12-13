"""
Router para endpoints de Voluntario
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas.voluntario import (
    VoluntarioCreate,
    VoluntarioUpdate,
    VoluntarioResponse,
    VoluntarioConEdad,
    SkillCreate,
    SkillResponse
)
from app.schemas.common import PaginatedResponse, DeleteResponse, CascadeInfo
from app.crud import voluntario as crud
from app.crud.cascade import count_cascade_deletes

router = APIRouter()


@router.post("/voluntarios", response_model=VoluntarioResponse, status_code=status.HTTP_201_CREATED)
def create_voluntario(voluntario: VoluntarioCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo voluntario.
    Valida que tenga al menos 18 años en la fecha de alta.
    """
    # Verificar que no existe
    db_voluntario = crud.get_voluntario(db, dni=voluntario.dni)
    if db_voluntario:
        raise HTTPException(status_code=400, detail="El voluntario ya existe")
    
    try:
        return crud.create_voluntario(db=db, voluntario=voluntario)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/voluntarios", response_model=PaginatedResponse[VoluntarioResponse])
def list_voluntarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista todos los voluntarios con paginación"""
    items, total = crud.get_voluntarios(db, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/voluntarios/{dni}/edad", response_model=VoluntarioConEdad)
def get_voluntario_con_edad(dni: str, db: Session = Depends(get_db)):
    """Obtiene un voluntario con edad calculada desde la vista"""
    db_voluntario = crud.get_voluntario_con_edad(db, dni=dni)
    if not db_voluntario:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")
    return db_voluntario


@router.get("/voluntarios/{dni}", response_model=VoluntarioResponse)
def get_voluntario(dni: str, db: Session = Depends(get_db)):
    """Obtiene un voluntario por DNI"""
    db_voluntario = crud.get_voluntario(db, dni=dni)
    if not db_voluntario:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")
    return db_voluntario


@router.put("/voluntarios/{dni}", response_model=VoluntarioResponse)
def update_voluntario(
    dni: str,
    voluntario: VoluntarioUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un voluntario"""
    db_voluntario = crud.update_voluntario(db, dni=dni, voluntario=voluntario)
    if not db_voluntario:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")
    return db_voluntario


@router.delete("/voluntarios/{dni}", response_model=DeleteResponse)
def delete_voluntario(dni: str, db: Session = Depends(get_db)):
    """
    Elimina un voluntario y todos sus registros relacionados en cascada.
    ADVERTENCIA: Esto eliminará skills, participaciones, coordinaciones y cesiones.
    """
    # Verificar que existe
    db_voluntario = crud.get_voluntario(db, dni=dni)
    if not db_voluntario:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")
    
    # Contar registros en cascada
    cascade_info = count_cascade_deletes(db, "voluntario", dni)
    
    # Eliminar
    success = crud.delete_voluntario(db, dni=dni)
    if not success:
        raise HTTPException(status_code=500, detail="Error al eliminar el voluntario")
    
    return DeleteResponse(
        message="Voluntario eliminado exitosamente",
        deleted_id=dni,
        cascade_info=CascadeInfo(**cascade_info)
    )


# Endpoints para skills de voluntario

@router.get("/voluntarios/{dni}/skills", response_model=List[SkillResponse])
def get_skills_voluntario(dni: str, db: Session = Depends(get_db)):
    """Lista los skills de un voluntario"""
    # Verificar que el voluntario existe
    db_voluntario = crud.get_voluntario(db, dni=dni)
    if not db_voluntario:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")
    
    return crud.get_skills_voluntario(db, dni_voluntario=dni)


@router.post(
    "/voluntarios/{dni}/skills",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED
)
def add_skill_voluntario(
    dni: str,
    skill: SkillCreate,
    db: Session = Depends(get_db)
):
    """Agrega un skill a un voluntario"""
    # Verificar que el voluntario existe
    db_voluntario = crud.get_voluntario(db, dni=dni)
    if not db_voluntario:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")
    
    try:
        return crud.add_skill_voluntario(db, dni_voluntario=dni, skill=skill)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al agregar skill: {str(e)}")


@router.delete("/voluntarios/{dni}/skills/{nombre_skill}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill_voluntario(dni: str, nombre_skill: str, db: Session = Depends(get_db)):
    """Elimina un skill de un voluntario"""
    success = crud.delete_skill_voluntario(db, dni_voluntario=dni, nombre_skill=nombre_skill)
    if not success:
        raise HTTPException(status_code=404, detail="Skill no encontrado")
    
    return None
