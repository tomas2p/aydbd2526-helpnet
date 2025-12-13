"""
Router para endpoints de Actividad
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.proyecto import ActividadCreate, ActividadUpdate, ActividadResponse
from app.schemas.common import PaginatedResponse, DeleteResponse, CascadeInfo
from app.crud import proyecto as crud
from app.crud.cascade import count_cascade_deletes

router = APIRouter()


@router.post(
    "/proyectos/{id_proyecto}/actividades",
    response_model=ActividadResponse,
    status_code=status.HTTP_201_CREATED
)
def create_actividad(
    id_proyecto: int,
    actividad: ActividadCreate,
    db: Session = Depends(get_db)
):
    """Crea una nueva actividad en un proyecto"""
    # Verificar que el proyecto existe
    db_proyecto = crud.get_proyecto(db, id_proyecto=id_proyecto)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    return crud.create_actividad(db=db, id_proyecto=id_proyecto, actividad=actividad)


@router.get(
    "/proyectos/{id_proyecto}/actividades",
    response_model=PaginatedResponse[ActividadResponse]
)
def list_actividades(
    id_proyecto: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista todas las actividades de un proyecto"""
    # Verificar que el proyecto existe
    db_proyecto = crud.get_proyecto(db, id_proyecto=id_proyecto)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    items, total = crud.get_actividades_proyecto(db, id_proyecto=id_proyecto, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get(
    "/proyectos/{id_proyecto}/actividades/{id_actividad}",
    response_model=ActividadResponse
)
def get_actividad(
    id_proyecto: int,
    id_actividad: int,
    db: Session = Depends(get_db)
):
    """Obtiene una actividad específica"""
    db_actividad = crud.get_actividad(db, id_actividad=id_actividad, id_proyecto=id_proyecto)
    if not db_actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return db_actividad


@router.put(
    "/proyectos/{id_proyecto}/actividades/{id_actividad}",
    response_model=ActividadResponse
)
def update_actividad(
    id_proyecto: int,
    id_actividad: int,
    actividad: ActividadUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza una actividad"""
    db_actividad = crud.update_actividad(
        db, id_actividad=id_actividad, id_proyecto=id_proyecto, actividad=actividad
    )
    if not db_actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return db_actividad


@router.delete(
    "/proyectos/{id_proyecto}/actividades/{id_actividad}",
    response_model=DeleteResponse
)
def delete_actividad(
    id_proyecto: int,
    id_actividad: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una actividad y todos sus registros relacionados en cascada.
    ADVERTENCIA: Esto eliminará localizaciones, participaciones y coordinaciones.
    """
    # Verificar que existe
    db_actividad = crud.get_actividad(db, id_actividad=id_actividad, id_proyecto=id_proyecto)
    if not db_actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    
    # Contar cascada
    cascade_info = count_cascade_deletes(db, "actividad", id_actividad)
    
    # Eliminar
    success = crud.delete_actividad(db, id_actividad=id_actividad, id_proyecto=id_proyecto)
    if not success:
        raise HTTPException(status_code=500, detail="Error al eliminar la actividad")
    
    return DeleteResponse(
        message="Actividad eliminada exitosamente",
        deleted_id=f"{id_actividad} (proyecto: {id_proyecto})",
        cascade_info=CascadeInfo(**cascade_info)
    )
