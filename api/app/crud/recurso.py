"""
CRUD para Recurso con herencia polimórfica (Donado/Alquilado)
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.recurso import Recurso, Donado, Alquilado
from app.schemas.recurso import RecursoDonandoCreate, RecursoAlquiladoCreate


# ============= RECURSO (Polimórfico) =============

def get_recurso(db: Session, id_recurso: int):
    """Obtiene un recurso por ID (polimórfico)"""
    return db.query(Recurso).filter(Recurso.id_recurso == id_recurso).first()


def get_recursos(
    db: Session,
    tipo: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
) -> tuple[List[Recurso], int]:
    """
    Lista recursos con paginación y filtro opcional por tipo
    tipo: 'D' para donados, 'A' para alquilados, None para todos
    """
    query = db.query(Recurso)
    
    if tipo == 'A':
        query = db.query(Alquilado)
    elif tipo == 'D':
        query = db.query(Donado)
    else:
        query = db.query(Recurso)
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def create_recurso_donado(db: Session, recurso: RecursoDonandoCreate) -> Donado:
    """Crea un recurso donado"""
    # Con herencia polimórfica, solo creamos la instancia de la subclase
    db_donado = Donado(
        nombre=recurso.nombre,
        descripcion=recurso.descripcion,
        fecha_entrega=recurso.fecha_entrega,
        tipo='D',
        estado=recurso.estado,
        nombre_donante=recurso.nombre_donante,
        email_donante=recurso.email_donante
    )
    db.add(db_donado)
    db.commit()
    db.refresh(db_donado)
    return db_donado


def create_recurso_alquilado(db: Session, recurso: RecursoAlquiladoCreate) -> Alquilado:
    """Crea un recurso alquilado"""
    # Con herencia polimórfica, solo creamos la instancia de la subclase
    db_alquilado = Alquilado(
        nombre=recurso.nombre,
        descripcion=recurso.descripcion,
        fecha_entrega=recurso.fecha_entrega,
        tipo='A',
        proveedor=recurso.proveedor,
        costo=recurso.costo,
        fecha_devolucion=recurso.fecha_devolucion
    )
    db.add(db_alquilado)
    db.commit()
    db.refresh(db_alquilado)
    return db_alquilado


def update_recurso_donado(db: Session, id_recurso: int, estado: str) -> Optional[Donado]:
    """Actualiza el estado de un recurso donado"""
    db_donado = db.query(Donado).filter(Donado.id_recurso == id_recurso).first()
    if not db_donado:
        return None
    
    db_donado.estado = estado
    db.commit()
    db.refresh(db_donado)
    return db_donado


def update_recurso_alquilado(db: Session, id_recurso: int, costo: float, fecha_devolucion) -> Optional[Alquilado]:
    """Actualiza un recurso alquilado"""
    db_alquilado = db.query(Alquilado).filter(Alquilado.id_recurso == id_recurso).first()
    if not db_alquilado:
        return None
    
    if costo is not None:
        db_alquilado.costo = costo
    if fecha_devolucion is not None:
        db_alquilado.fecha_devolucion = fecha_devolucion
    
    db.commit()
    db.refresh(db_alquilado)
    return db_alquilado


def delete_recurso(db: Session, id_recurso: int) -> bool:
    """Elimina un recurso (cualquier tipo, CASCADE a tabla hija)"""
    db_recurso = db.query(Recurso).filter(Recurso.id_recurso == id_recurso).first()
    if not db_recurso:
        return False
    
    db.delete(db_recurso)
    db.commit()
    return True
