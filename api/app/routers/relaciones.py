"""
Router para endpoints de relaciones N:M y ternarias
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas.relaciones import (
    ParticipaCreate,
    ParticipaUpdate,
    ParticipaResponse,
    CoordinaCreate,
    CoordinaResponse,
    CesionCreate,
    CesionResponse,
    RecursoUsadoCreate,
    RecursoUsadoResponse
)
from app.schemas.common import PaginatedResponse
from app.crud import relaciones as crud

router = APIRouter()


# ============= PARTICIPA =============

@router.post("/participaciones", response_model=ParticipaResponse, status_code=status.HTTP_201_CREATED)
def create_participacion(participa: ParticipaCreate, db: Session = Depends(get_db)):
    """Asigna un voluntario a una localización con rol operativo"""
    try:
        return crud.create_participa(db=db, participa=participa)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear participación: {str(e)}")


@router.get("/participaciones", response_model=PaginatedResponse[ParticipaResponse])
def list_participaciones(
    dni_voluntario: str = Query(None, description="Filtrar por DNI de voluntario"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista participaciones con filtros opcionales"""
    if dni_voluntario:
        items = crud.get_participaciones_voluntario(db, dni_voluntario=dni_voluntario)
        total = len(items)
        items = items[skip:skip+limit]
    else:
        items, total = crud.get_participaciones(db, skip=skip, limit=limit)
    
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.delete(
    "/participaciones/{id_localizacion}/{id_actividad}/{id_proyecto}/{dni_voluntario}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_participacion(
    id_localizacion: str,
    id_actividad: str,
    id_proyecto: str,
    dni_voluntario: str,
    db: Session = Depends(get_db)
):
    """Elimina una participación"""
    success = crud.delete_participa(
        db,
        id_localizacion=id_localizacion,
        id_actividad=id_actividad,
        id_proyecto=id_proyecto,
        dni_voluntario=dni_voluntario
    )
    if not success:
        raise HTTPException(status_code=404, detail="Participación no encontrada")
    
    return None


# ============= COORDINA =============

@router.post("/coordinaciones", response_model=CoordinaResponse, status_code=status.HTTP_201_CREATED)
def create_coordinacion(coordina: CoordinaCreate, db: Session = Depends(get_db)):
    """Asigna un voluntario como coordinador de una localización"""
    try:
        return crud.create_coordina(db=db, coordina=coordina)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear coordinación: {str(e)}")


@router.get("/coordinaciones", response_model=PaginatedResponse[CoordinaResponse])
def list_coordinaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista coordinaciones"""
    items, total = crud.get_coordinaciones(db, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.delete(
    "/coordinaciones/{id_localizacion}/{id_actividad}/{id_proyecto}/{dni_voluntario}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_coordinacion(
    id_localizacion: str,
    id_actividad: str,
    id_proyecto: str,
    dni_voluntario: str,
    db: Session = Depends(get_db)
):
    """Elimina una coordinación"""
    success = crud.delete_coordina(
        db,
        id_localizacion=id_localizacion,
        id_actividad=id_actividad,
        id_proyecto=id_proyecto,
        dni_voluntario=dni_voluntario
    )
    if not success:
        raise HTTPException(status_code=404, detail="Coordinación no encontrada")
    
    return None


# ============= CESIÓN (Ternaria) =============

@router.post("/cesiones", response_model=CesionResponse, status_code=status.HTTP_201_CREATED)
def create_cesion(cesion: CesionCreate, db: Session = Depends(get_db)):
    """Crea una cesión de voluntario entre organización y proyecto"""
    try:
        return crud.create_cesion(db=db, cesion=cesion)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear cesión: {str(e)}")


@router.get("/cesiones", response_model=PaginatedResponse[CesionResponse])
def list_cesiones(
    nombre_organizacion: str = Query(None, description="Filtrar por organización"),
    id_proyecto: str = Query(None, description="Filtrar por proyecto"),
    dni_voluntario: str = Query(None, description="Filtrar por voluntario"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista cesiones con filtros opcionales"""
    items, total = crud.get_cesiones(db, skip=skip, limit=limit)
    
    # Aplicar filtros manuales (optimización: hacer en query SQL)
    if nombre_organizacion:
        items = [item for item in items if item.nombre_organizacion == nombre_organizacion]
    if id_proyecto:
        items = [item for item in items if item.id_proyecto == id_proyecto]
    if dni_voluntario:
        items = [item for item in items if item.dni_voluntario == dni_voluntario]
    
    total = len(items)
    items = items[skip:skip+limit]
    
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.delete(
    "/cesiones/{nombre_organizacion}/{id_proyecto}/{dni_voluntario}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_cesion(
    nombre_organizacion: str,
    id_proyecto: str,
    dni_voluntario: str,
    db: Session = Depends(get_db)
):
    """Elimina una cesión"""
    success = crud.delete_cesion(
        db,
        nombre_organizacion=nombre_organizacion,
        id_proyecto=id_proyecto,
        dni_voluntario=dni_voluntario
    )
    if not success:
        raise HTTPException(status_code=404, detail="Cesión no encontrada")
    
    return None


# ============= RECURSO_USADO =============

@router.post(
    "/proyectos/{id_proyecto}/recursos",
    response_model=RecursoUsadoResponse,
    status_code=status.HTTP_201_CREATED
)
def assign_recurso_proyecto(
    id_proyecto: str,
    id_recurso: int = Query(..., description="ID del recurso a asignar"),
    db: Session = Depends(get_db)
):
    """Asigna un recurso a un proyecto"""
    recurso_usado = RecursoUsadoCreate(id_proyecto=id_proyecto, id_recurso=id_recurso)
    try:
        return crud.create_recurso_usado(db=db, recurso_usado=recurso_usado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al asignar recurso: {str(e)}")


@router.get("/proyectos/{id_proyecto}/recursos", response_model=List[RecursoUsadoResponse])
def list_recursos_proyecto(id_proyecto: str, db: Session = Depends(get_db)):
    """Lista recursos usados en un proyecto"""
    return crud.get_recursos_usados_proyecto(db, id_proyecto=id_proyecto)


@router.delete(
    "/proyectos/{id_proyecto}/recursos/{id_recurso}",
    status_code=status.HTTP_204_NO_CONTENT
)
def unassign_recurso_proyecto(
    id_proyecto: str,
    id_recurso: int,
    db: Session = Depends(get_db)
):
    """Desasigna un recurso de un proyecto"""
    success = crud.delete_recurso_usado(db, id_proyecto=id_proyecto, id_recurso=id_recurso)
    if not success:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    
    return None
