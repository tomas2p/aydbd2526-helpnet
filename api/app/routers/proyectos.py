"""
Router para endpoints de Proyecto
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate, ProyectoResponse
from app.schemas.common import PaginatedResponse, DeleteResponse, CascadeInfo
from app.crud import proyecto as crud
from app.crud import organizacion as org_crud
from app.crud.cascade import count_cascade_deletes

router = APIRouter()


@router.post("/proyectos", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED)
def create_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo proyecto"""
    # Verificar que la organización existe
    if proyecto.nombre_organizacion:
        db_org = org_crud.get_organizacion(db, nombre=proyecto.nombre_organizacion)
        if not db_org:
            raise HTTPException(status_code=404, detail="Organización no encontrada")
    
    return crud.create_proyecto(db=db, proyecto=proyecto)


@router.get("/proyectos", response_model=PaginatedResponse[ProyectoResponse])
def list_proyectos(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista todos los proyectos con paginación"""
    items, total = crud.get_proyectos(db, skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/proyectos/{id_proyecto}", response_model=ProyectoResponse)
def get_proyecto(id_proyecto: int, db: Session = Depends(get_db)):
    """Obtiene un proyecto por ID"""
    db_proyecto = crud.get_proyecto(db, id_proyecto=id_proyecto)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_proyecto


@router.put("/proyectos/{id_proyecto}", response_model=ProyectoResponse)
def update_proyecto(
    id_proyecto: int,
    proyecto: ProyectoUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un proyecto"""
    db_proyecto = crud.update_proyecto(db, id_proyecto=id_proyecto, proyecto=proyecto)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_proyecto


@router.delete("/proyectos/{id_proyecto}", response_model=DeleteResponse)
def delete_proyecto(id_proyecto: int, db: Session = Depends(get_db)):
    """
    Elimina un proyecto y todos sus registros relacionados en cascada.
    ADVERTENCIA: Esto eliminará actividades, localizaciones, participaciones, etc.
    """
    # Verificar que existe
    db_proyecto = crud.get_proyecto(db, id_proyecto=id_proyecto)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Contar registros en cascada
    cascade_info = count_cascade_deletes(db, "proyecto", id_proyecto)
    
    # Eliminar
    success = crud.delete_proyecto(db, id_proyecto=id_proyecto)
    if not success:
        raise HTTPException(status_code=500, detail="Error al eliminar el proyecto")
    
    return DeleteResponse(
        message="Proyecto eliminado exitosamente",
        deleted_id=id_proyecto,
        cascade_info=CascadeInfo(**cascade_info)
    )
