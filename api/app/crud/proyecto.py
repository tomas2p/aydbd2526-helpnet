"""
CRUD para Proyecto, Actividad y Localización
"""
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models.proyecto import Proyecto, Actividad, Localizacion
from app.schemas.proyecto import (
    ProyectoCreate, ProyectoUpdate,
    ActividadCreate, ActividadUpdate,
    LocalizacionCreate, LocalizacionUpdate
)


# ============= PROYECTO =============

def get_proyecto(db: Session, id_proyecto: int) -> Optional[Proyecto]:
    """Obtiene un proyecto por ID"""
    return db.query(Proyecto).options(
        joinedload(Proyecto.actividades)
    ).filter(Proyecto.id_proyecto == id_proyecto).first()


def get_proyectos(db: Session, skip: int = 0, limit: int = 20) -> tuple[List[Proyecto], int]:
    """Lista proyectos con paginación"""
    query = db.query(Proyecto)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def create_proyecto(db: Session, proyecto: ProyectoCreate) -> Proyecto:
    """Crea un nuevo proyecto"""
    db_proyecto = Proyecto(**proyecto.model_dump())
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto


def update_proyecto(db: Session, id_proyecto: int, proyecto: ProyectoUpdate) -> Optional[Proyecto]:
    """Actualiza un proyecto"""
    db_proyecto = db.query(Proyecto).filter(Proyecto.id_proyecto == id_proyecto).first()
    if not db_proyecto:
        return None
    
    update_data = proyecto.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_proyecto, field, value)
    
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto


def delete_proyecto(db: Session, id_proyecto: int) -> bool:
    """Elimina un proyecto"""
    db_proyecto = db.query(Proyecto).filter(Proyecto.id_proyecto == id_proyecto).first()
    if not db_proyecto:
        return False
    
    db.delete(db_proyecto)
    db.commit()
    return True


# ============= ACTIVIDAD =============

def get_actividad(db: Session, id_actividad: int, id_proyecto: int) -> Optional[Actividad]:
    """Obtiene una actividad por ID compuesto"""
    return db.query(Actividad).filter(
        Actividad.id_actividad == id_actividad,
        Actividad.id_proyecto == id_proyecto
    ).first()


def get_actividades_proyecto(db: Session, id_proyecto: int, skip: int = 0, limit: int = 20) -> tuple[List[Actividad], int]:
    """Lista actividades de un proyecto"""
    query = db.query(Actividad).filter(Actividad.id_proyecto == id_proyecto)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def create_actividad(db: Session, id_proyecto: int, actividad: ActividadCreate) -> Actividad:
    """Crea una nueva actividad"""
    db_actividad = Actividad(
        id_proyecto=id_proyecto,
        **actividad.model_dump()
    )
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)
    return db_actividad


def update_actividad(db: Session, id_actividad: int, id_proyecto: int, actividad: ActividadUpdate) -> Optional[Actividad]:
    """Actualiza una actividad"""
    db_actividad = get_actividad(db, id_actividad, id_proyecto)
    if not db_actividad:
        return None
    
    update_data = actividad.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_actividad, field, value)
    
    db.commit()
    db.refresh(db_actividad)
    return db_actividad


def delete_actividad(db: Session, id_actividad: int, id_proyecto: int) -> bool:
    """Elimina una actividad"""
    db_actividad = get_actividad(db, id_actividad, id_proyecto)
    if not db_actividad:
        return False
    
    db.delete(db_actividad)
    db.commit()
    return True


# ============= LOCALIZACIÓN =============

def get_localizacion(
    db: Session,
    id_localizacion: int,
    id_actividad: int,
    id_proyecto: int
) -> Optional[Localizacion]:
    """Obtiene una localización por ID compuesto (3 campos)"""
    return db.query(Localizacion).filter(
        Localizacion.id_localizacion == id_localizacion,
        Localizacion.id_actividad == id_actividad,
        Localizacion.id_proyecto == id_proyecto
    ).first()


def get_localizaciones_actividad(
    db: Session,
    id_actividad: int,
    id_proyecto: int,
    skip: int = 0,
    limit: int = 20
) -> tuple[List[Localizacion], int]:
    """Lista localizaciones de una actividad"""
    query = db.query(Localizacion).filter(
        Localizacion.id_actividad == id_actividad,
        Localizacion.id_proyecto == id_proyecto
    )
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def create_localizacion(
    db: Session,
    id_actividad: int,
    id_proyecto: int,
    localizacion: LocalizacionCreate
) -> Localizacion:
    """Crea una nueva localización"""
    db_localizacion = Localizacion(
        id_actividad=id_actividad,
        id_proyecto=id_proyecto,
        **localizacion.model_dump()
    )
    db.add(db_localizacion)
    db.commit()
    db.refresh(db_localizacion)
    return db_localizacion


def update_localizacion(
    db: Session,
    id_localizacion: int,
    id_actividad: int,
    id_proyecto: int,
    localizacion: LocalizacionUpdate
) -> Optional[Localizacion]:
    """Actualiza una localización"""
    db_localizacion = get_localizacion(db, id_localizacion, id_actividad, id_proyecto)
    if not db_localizacion:
        return None
    
    update_data = localizacion.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_localizacion, field, value)
    
    db.commit()
    db.refresh(db_localizacion)
    return db_localizacion


def delete_localizacion(
    db: Session,
    id_localizacion: int,
    id_actividad: int,
    id_proyecto: int
) -> bool:
    """Elimina una localización"""
    db_localizacion = get_localizacion(db, id_localizacion, id_actividad, id_proyecto)
    if not db_localizacion:
        return False
    
    db.delete(db_localizacion)
    db.commit()
    return True
