"""
Router para endpoints de Recurso (polimórfico: Donado/Alquilado)
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional, Union

from app.dependencies import get_db
from app.schemas.recurso import (
    RecursoDonandoCreate,
    RecursoDonandoResponse,
    RecursoAlquiladoCreate,
    RecursoAlquiladoResponse,
    serialize_recurso
)
from app.schemas.common import PaginatedResponse, DeleteResponse, CascadeInfo
from app.crud import recurso as crud
from app.models.relaciones import RecursoUsado

router = APIRouter()


@router.post(
    "/recursos",
    response_model=Union[RecursoDonandoResponse, RecursoAlquiladoResponse],
    status_code=status.HTTP_201_CREATED
)
def create_recurso(
    recurso: Union[RecursoDonandoCreate, RecursoAlquiladoCreate],
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo recurso (donado o alquilado).
    El tipo se discrimina automáticamente por el campo 'tipo' en el body.
    - tipo='D': Recurso donado
    - tipo='A': Recurso alquilado
    """
    if recurso.tipo == 'D':
        return crud.create_recurso_donado(db=db, recurso=recurso)
    elif recurso.tipo == 'A':
        return crud.create_recurso_alquilado(db=db, recurso=recurso)
    else:
        raise HTTPException(status_code=400, detail="Tipo de recurso inválido. Use 'D' o 'A'")


@router.get(
    "/recursos",
    response_model=PaginatedResponse[Union[RecursoDonandoResponse, RecursoAlquiladoResponse]]
)
def list_recursos(
    tipo: Optional[str] = Query(None, pattern="^[DA]$", description="Filtrar por tipo: D=Donado, A=Alquilado"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Lista todos los recursos con paginación.
    Opcionalmente filtra por tipo (D=Donado, A=Alquilado).
    Retorna una lista heterogénea con recursos donados y alquilados serializados dinámicamente.
    """
    items, total = crud.get_recursos(db, tipo=tipo, skip=skip, limit=limit)
    
    # Serializar cada recurso según su tipo
    serialized_items = [serialize_recurso(item) for item in items]
    
    return PaginatedResponse(items=serialized_items, total=total, skip=skip, limit=limit)


# Endpoints específicos para recursos donados (debe ir antes de /recursos/{id_recurso})

@router.get("/recursos/donados", response_model=PaginatedResponse[RecursoDonandoResponse])
def list_recursos_donados(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista solo recursos donados"""
    items, total = crud.get_recursos(db, tipo='D', skip=skip, limit=limit)
    serialized_items = [serialize_recurso(item) for item in items]
    return PaginatedResponse(items=serialized_items, total=total, skip=skip, limit=limit)


# Endpoints específicos para recursos alquilados (debe ir antes de /recursos/{id_recurso})

@router.get("/recursos/alquilados", response_model=PaginatedResponse[RecursoAlquiladoResponse])
def list_recursos_alquilados(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista solo recursos alquilados"""
    items, total = crud.get_recursos(db, tipo='A', skip=skip, limit=limit)
    serialized_items = [serialize_recurso(item) for item in items]
    return PaginatedResponse(items=serialized_items, total=total, skip=skip, limit=limit)


@router.get(
    "/recursos/{id_recurso}",
    response_model=Union[RecursoDonandoResponse, RecursoAlquiladoResponse]
)
def get_recurso(id_recurso: int, db: Session = Depends(get_db)):
    """Obtiene un recurso por ID (retorna tipo específico según discriminador)"""
    db_recurso = crud.get_recurso(db, id_recurso=id_recurso)
    if not db_recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    
    return serialize_recurso(db_recurso)


@router.delete("/recursos/{id_recurso}", response_model=DeleteResponse)
def delete_recurso(id_recurso: int, db: Session = Depends(get_db)):
    """
    Elimina un recurso (donado o alquilado).
    ADVERTENCIA: Eliminará también las asignaciones a proyectos.
    """
    # Verificar que existe
    db_recurso = crud.get_recurso(db, id_recurso=id_recurso)
    if not db_recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    
    # Contar recursos_usados que serán eliminados
    recursos_usados_count = db.query(RecursoUsado).filter(
        RecursoUsado.id_recurso == id_recurso
    ).count()
    
    # Eliminar
    success = crud.delete_recurso(db, id_recurso=id_recurso)
    if not success:
        raise HTTPException(status_code=500, detail="Error al eliminar el recurso")
    
    cascade_info = {"recursos_usados": recursos_usados_count}
    
    return DeleteResponse(
        message="Recurso eliminado exitosamente",
        deleted_id=id_recurso,
        cascade_info=CascadeInfo(**cascade_info)
    )
