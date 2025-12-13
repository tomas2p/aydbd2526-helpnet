"""
CRUD para Organización y EmailOrganizacion
"""
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models.organizacion import Organizacion, EmailOrganizacion
from app.schemas.organizacion import OrganizacionCreate, OrganizacionUpdate


def get_organizacion(db: Session, nombre: str) -> Optional[Organizacion]:
    """Obtiene una organización por nombre con sus emails"""
    return db.query(Organizacion).options(
        joinedload(Organizacion.emails)
    ).filter(Organizacion.nombre == nombre).first()


def get_organizaciones(db: Session, skip: int = 0, limit: int = 20) -> tuple[List[Organizacion], int]:
    """Lista organizaciones con paginación"""
    query = db.query(Organizacion).options(joinedload(Organizacion.emails))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def create_organizacion(db: Session, org: OrganizacionCreate) -> Organizacion:
    """Crea una nueva organización con sus emails"""
    db_org = Organizacion(nombre=org.nombre, tipo=org.tipo)
    db.add(db_org)
    db.flush()
    
    # Agregar emails
    for email in org.emails:
        db_email = EmailOrganizacion(nombre_organizacion=org.nombre, email=email)
        db.add(db_email)
    
    db.commit()
    db.refresh(db_org)
    return db_org


def update_organizacion(db: Session, nombre: str, org: OrganizacionUpdate) -> Optional[Organizacion]:
    """Actualiza una organización"""
    db_org = db.query(Organizacion).filter(Organizacion.nombre == nombre).first()
    if not db_org:
        return None
    
    if org.tipo is not None:
        db_org.tipo = org.tipo
    
    db.commit()
    db.refresh(db_org)
    return db_org


def delete_organizacion(db: Session, nombre: str) -> bool:
    """Elimina una organización (con CASCADE automático)"""
    db_org = db.query(Organizacion).filter(Organizacion.nombre == nombre).first()
    if not db_org:
        return False
    
    db.delete(db_org)
    db.commit()
    return True


def add_email_organizacion(db: Session, nombre_org: str, email: str) -> EmailOrganizacion:
    """Agrega un email a una organización"""
    db_email = EmailOrganizacion(nombre_organizacion=nombre_org, email=email)
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email


def delete_email_organizacion(db: Session, nombre_org: str, email: str) -> bool:
    """Elimina un email de una organización"""
    db_email = db.query(EmailOrganizacion).filter(
        EmailOrganizacion.nombre_organizacion == nombre_org,
        EmailOrganizacion.email == email
    ).first()
    
    if not db_email:
        return False
    
    db.delete(db_email)
    db.commit()
    return True
