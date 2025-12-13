"""
Router para endpoints de Localización
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.proyecto import LocalizacionCreate, LocalizacionUpdate, LocalizacionResponse
from app.schemas.common import PaginatedResponse, DeleteResponse, CascadeInfo
from app.crud import proyecto as crud
from app.models.relaciones import Participa, Coordina

router = APIRouter()


@router.post(
    "/proyectos/{id_proyecto}/actividades/{id_actividad}/localizaciones",
    response_model=LocalizacionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_localizacion(
    id_proyecto: int,
    id_actividad: int,
    localizacion: LocalizacionCreate,
    db: Session = Depends(get_db)
):
    """Crea una nueva localización en una actividad"""
    # Verificar que la actividad existe
    db_actividad = crud.get_actividad(db, id_actividad=id_actividad, id_proyecto=id_proyecto)
    if not db_actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    
    return crud.create_localizacion(
        db=db,
        id_actividad=id_actividad,
        id_proyecto=id_proyecto,
        localizacion=localizacion
    )


@router.get(
    "/proyectos/{id_proyecto}/actividades/{id_actividad}/localizaciones",
    response_model=PaginatedResponse[LocalizacionResponse]
)
def list_localizaciones(
    id_proyecto: int,
    id_actividad: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista todas las localizaciones de una actividad"""
    items, total = crud.get_localizaciones_actividad(
        db, id_actividad=id_actividad, id_proyecto=id_proyecto, skip=skip, limit=limit
    )
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get(
    "/proyectos/{id_proyecto}/actividades/{id_actividad}/localizaciones/{id_localizacion}",
    response_model=LocalizacionResponse
)
def get_localizacion(
    id_proyecto: int,
    id_actividad: int,
    id_localizacion: int,
    db: Session = Depends(get_db)
):
    """Obtiene una localización específica"""
    db_localizacion = crud.get_localizacion(
        db,
        id_localizacion=id_localizacion,
        id_actividad=id_actividad,
        id_proyecto=id_proyecto
    )
    if not db_localizacion:
        raise HTTPException(status_code=404, detail="Localización no encontrada")
    return db_localizacion


@router.put(
    "/proyectos/{id_proyecto}/actividades/{id_actividad}/localizaciones/{id_localizacion}",
    response_model=LocalizacionResponse
)
def update_localizacion(
    id_proyecto: int,
    id_actividad: int,
    id_localizacion: int,
    localizacion: LocalizacionUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza una localización"""
    db_localizacion = crud.update_localizacion(
        db,
        id_localizacion=id_localizacion,
        id_actividad=id_actividad,
        id_proyecto=id_proyecto,
        localizacion=localizacion
    )
    if not db_localizacion:
        raise HTTPException(status_code=404, detail="Localización no encontrada")
    return db_localizacion


@router.delete(
    "/proyectos/{id_proyecto}/actividades/{id_actividad}/localizaciones/{id_localizacion}",
    response_model=DeleteResponse
)
def delete_localizacion(
    id_proyecto: int,
    id_actividad: int,
    id_localizacion: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una localización y todos sus registros relacionados en cascada.
    ADVERTENCIA: Esto eliminará participaciones y coordinaciones.
    """
    # Verificar que existe
    db_localizacion = crud.get_localizacion(
        db,
        id_localizacion=id_localizacion,
        id_actividad=id_actividad,
        id_proyecto=id_proyecto
    )
    if not db_localizacion:
        raise HTTPException(status_code=404, detail="Localización no encontrada")
    
    # Contar participaciones y coordinaciones
    participaciones_count = db.query(Participa).filter(
        Participa.id_localizacion == id_localizacion,
        Participa.id_actividad == id_actividad,
        Participa.id_proyecto == id_proyecto
    ).count()
    
    coordinaciones_count = db.query(Coordina).filter(
        Coordina.id_localizacion == id_localizacion,
        Coordina.id_actividad == id_actividad,
        Coordina.id_proyecto == id_proyecto
    ).count()
    
    # Eliminar
    success = crud.delete_localizacion(
        db,
        id_localizacion=id_localizacion,
        id_actividad=id_actividad,
        id_proyecto=id_proyecto
    )
    if not success:
        raise HTTPException(status_code=500, detail="Error al eliminar la localización")
    
    cascade_info = {
        "participaciones": participaciones_count,
        "coordinaciones": coordinaciones_count
    }
    
    return DeleteResponse(
        message="Localización eliminada exitosamente",
        deleted_id=f"{id_localizacion} (actividad: {id_actividad}, proyecto: {id_proyecto})",
        cascade_info=CascadeInfo(**cascade_info)
    )
