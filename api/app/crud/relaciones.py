"""
CRUD para relaciones N:M y ternarias
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.relaciones import Participa, Coordina, Cesion, RecursoUsado
from app.schemas.relaciones import (
    ParticipaCreate, ParticipaUpdate,
    CoordinaCreate, CoordinaUpdate,
    CesionCreate, CesionUpdate,
    RecursoUsadoCreate
)


# ============= PARTICIPA =============

def get_participa(
    db: Session,
    id_localizacion: int,
    id_actividad: int,
    id_proyecto: int,
    dni_voluntario: str
) -> Optional[Participa]:
    """Obtiene una participación específica"""
    return db.query(Participa).filter(
        Participa.id_localizacion == id_localizacion,
        Participa.id_actividad == id_actividad,
        Participa.id_proyecto == id_proyecto,
        Participa.dni_voluntario == dni_voluntario
    ).first()


def get_participaciones(db: Session, skip: int = 0, limit: int = 20) -> tuple[List[Participa], int]:
    """Lista todas las participaciones"""
    query = db.query(Participa)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def get_participaciones_voluntario(db: Session, dni_voluntario: str) -> List[Participa]:
    """Lista participaciones de un voluntario"""
    return db.query(Participa).filter(Participa.dni_voluntario == dni_voluntario).all()


def create_participa(db: Session, participa: ParticipaCreate) -> Participa:
    """Crea una nueva participación"""
    db_participa = Participa(**participa.model_dump())
    db.add(db_participa)
    db.commit()
    db.refresh(db_participa)
    return db_participa


def update_participa(
    db: Session,
    id_localizacion: int,
    id_actividad: int,
    id_proyecto: int,
    dni_voluntario: str,
    participa: ParticipaUpdate
) -> Optional[Participa]:
    """Actualiza una participación"""
    db_participa = get_participa(db, id_localizacion, id_actividad, id_proyecto, dni_voluntario)
    if not db_participa:
        return None
    
    update_data = participa.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_participa, field, value)
    
    db.commit()
    db.refresh(db_participa)
    return db_participa


def delete_participa(
    db: Session,
    id_localizacion: int,
    id_actividad: int,
    id_proyecto: int,
    dni_voluntario: str
) -> bool:
    """Elimina una participación"""
    db_participa = get_participa(db, id_localizacion, id_actividad, id_proyecto, dni_voluntario)
    if not db_participa:
        return False
    
    db.delete(db_participa)
    db.commit()
    return True


# ============= COORDINA =============

def get_coordina(
    db: Session,
    id_localizacion: int,
    id_actividad: int,
    id_proyecto: int,
    dni_voluntario: str
) -> Optional[Coordina]:
    """Obtiene una coordinación específica"""
    return db.query(Coordina).filter(
        Coordina.id_localizacion == id_localizacion,
        Coordina.id_actividad == id_actividad,
        Coordina.id_proyecto == id_proyecto,
        Coordina.dni_voluntario == dni_voluntario
    ).first()


def get_coordinaciones(db: Session, skip: int = 0, limit: int = 20) -> tuple[List[Coordina], int]:
    """Lista todas las coordinaciones"""
    query = db.query(Coordina)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def create_coordina(db: Session, coordina: CoordinaCreate) -> Coordina:
    """Crea una nueva coordinación"""
    db_coordina = Coordina(**coordina.model_dump())
    db.add(db_coordina)
    db.commit()
    db.refresh(db_coordina)
    return db_coordina


def delete_coordina(
    db: Session,
    id_localizacion: int,
    id_actividad: int,
    id_proyecto: int,
    dni_voluntario: str
) -> bool:
    """Elimina una coordinación"""
    db_coordina = get_coordina(db, id_localizacion, id_actividad, id_proyecto, dni_voluntario)
    if not db_coordina:
        return False
    
    db.delete(db_coordina)
    db.commit()
    return True


# ============= CESIÓN (Ternaria) =============

def get_cesion(
    db: Session,
    nombre_organizacion: str,
    id_proyecto: int,
    dni_voluntario: str
) -> Optional[Cesion]:
    """Obtiene una cesión específica"""
    return db.query(Cesion).filter(
        Cesion.nombre_organizacion == nombre_organizacion,
        Cesion.id_proyecto == id_proyecto,
        Cesion.dni_voluntario == dni_voluntario
    ).first()


def get_cesiones(db: Session, skip: int = 0, limit: int = 20) -> tuple[List[Cesion], int]:
    """Lista todas las cesiones"""
    query = db.query(Cesion)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def create_cesion(db: Session, cesion: CesionCreate) -> Cesion:
    """Crea una nueva cesión"""
    db_cesion = Cesion(**cesion.model_dump())
    db.add(db_cesion)
    db.commit()
    db.refresh(db_cesion)
    return db_cesion


def delete_cesion(
    db: Session,
    nombre_organizacion: str,
    id_proyecto: int,
    dni_voluntario: str
) -> bool:
    """Elimina una cesión"""
    db_cesion = get_cesion(db, nombre_organizacion, id_proyecto, dni_voluntario)
    if not db_cesion:
        return False
    
    db.delete(db_cesion)
    db.commit()
    return True


# ============= RECURSO_USADO =============

def create_recurso_usado(db: Session, recurso_usado: RecursoUsadoCreate) -> RecursoUsado:
    """Asigna un recurso a un proyecto"""
    db_recurso_usado = RecursoUsado(**recurso_usado.model_dump())
    db.add(db_recurso_usado)
    db.commit()
    db.refresh(db_recurso_usado)
    return db_recurso_usado


def get_recursos_usados_proyecto(db: Session, id_proyecto: str) -> List[RecursoUsado]:
    """Lista recursos usados en un proyecto"""
    return db.query(RecursoUsado).filter(RecursoUsado.id_proyecto == id_proyecto).all()


def delete_recurso_usado(db: Session, id_proyecto: str, id_recurso: int) -> bool:
    """Desasigna un recurso de un proyecto"""
    db_recurso_usado = db.query(RecursoUsado).filter(
        RecursoUsado.id_proyecto == id_proyecto,
        RecursoUsado.id_recurso == id_recurso
    ).first()
    
    if not db_recurso_usado:
        return False
    
    db.delete(db_recurso_usado)
    db.commit()
    return True
