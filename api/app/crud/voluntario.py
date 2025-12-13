"""
CRUD para Voluntario y VoluntarioSkill
"""
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models.voluntario import Voluntario, VoluntarioSkill, VistaVoluntarioEdad
from app.schemas.voluntario import VoluntarioCreate, VoluntarioUpdate, SkillCreate


# ============= VOLUNTARIO =============

def get_voluntario(db: Session, dni: str) -> Optional[Voluntario]:
    """Obtiene un voluntario por DNI"""
    return db.query(Voluntario).options(
        joinedload(Voluntario.skills)
    ).filter(Voluntario.dni == dni).first()


def get_voluntario_con_edad(db: Session, dni: str):
    """Obtiene un voluntario con edad calculada desde la vista o calculado dinámicamente"""
    from datetime import date
    
    # Primero intentar con la tabla de voluntarios
    voluntario = db.query(Voluntario).filter(Voluntario.dni == dni).first()
    if not voluntario:
        return None
    
    try:
        # Intentar usar la vista si existe
        vista_result = db.query(VistaVoluntarioEdad).filter(VistaVoluntarioEdad.dni == dni).first()
        if vista_result:
            return vista_result
    except Exception:
        pass
    
    # Si la vista no existe o no retornó resultado, calcular la edad manualmente
    edad = int((date.today() - voluntario.fecha_nacimiento).days / 365.25)
    voluntario.edad = edad
    return voluntario


def get_voluntarios(db: Session, skip: int = 0, limit: int = 20) -> tuple[List[Voluntario], int]:
    """Lista voluntarios con paginación"""
    query = db.query(Voluntario).options(joinedload(Voluntario.skills))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def create_voluntario(db: Session, voluntario: VoluntarioCreate) -> Voluntario:
    """Crea un nuevo voluntario"""
    db_voluntario = Voluntario(**voluntario.model_dump())
    db.add(db_voluntario)
    db.commit()
    db.refresh(db_voluntario)
    return db_voluntario


def update_voluntario(db: Session, dni: str, voluntario: VoluntarioUpdate) -> Optional[Voluntario]:
    """Actualiza un voluntario"""
    db_voluntario = db.query(Voluntario).filter(Voluntario.dni == dni).first()
    if not db_voluntario:
        return None
    
    update_data = voluntario.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_voluntario, field, value)
    
    db.commit()
    db.refresh(db_voluntario)
    return db_voluntario


def delete_voluntario(db: Session, dni: str) -> bool:
    """Elimina un voluntario"""
    db_voluntario = db.query(Voluntario).filter(Voluntario.dni == dni).first()
    if not db_voluntario:
        return False
    
    db.delete(db_voluntario)
    db.commit()
    return True


# ============= VOLUNTARIO SKILL =============

def get_skills_voluntario(db: Session, dni_voluntario: str) -> List[VoluntarioSkill]:
    """Lista skills de un voluntario"""
    return db.query(VoluntarioSkill).filter(
        VoluntarioSkill.dni_voluntario == dni_voluntario
    ).all()


def add_skill_voluntario(db: Session, dni_voluntario: str, skill: SkillCreate) -> VoluntarioSkill:
    """Agrega un skill a un voluntario"""
    db_skill = VoluntarioSkill(
        dni_voluntario=dni_voluntario,
        **skill.model_dump()
    )
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


def delete_skill_voluntario(db: Session, dni_voluntario: str, nombre_skill: str) -> bool:
    """Elimina un skill de un voluntario"""
    db_skill = db.query(VoluntarioSkill).filter(
        VoluntarioSkill.dni_voluntario == dni_voluntario,
        VoluntarioSkill.nombre_skill == nombre_skill
    ).first()
    
    if not db_skill:
        return False
    
    db.delete(db_skill)
    db.commit()
    return True
