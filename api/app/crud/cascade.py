"""
Utilidades para conteo de registros eliminados en cascada
"""
from sqlalchemy.orm import Session
from typing import Dict
from app.models import (
    Organizacion, Proyecto, Actividad, Localizacion,
    Voluntario, Participa, Coordina, Cesion,
    EmailOrganizacion, VoluntarioSkill, RecursoUsado
)


def count_cascade_deletes(db: Session, entity_type: str, entity_id: str) -> Dict[str, int]:
    """
    Cuenta los registros que serán eliminados en cascada
    
    Args:
        db: Sesión de base de datos
        entity_type: Tipo de entidad ('organizacion', 'proyecto', 'voluntario', etc.)
        entity_id: ID de la entidad a eliminar
    
    Returns:
        Diccionario con conteo de registros afectados por cascada
    """
    cascade_info = {}
    
    if entity_type == "organizacion":
        # Contar emails
        cascade_info["emails"] = db.query(EmailOrganizacion).filter(
            EmailOrganizacion.nombre_organizacion == entity_id
        ).count()
        
        # Contar proyectos
        proyectos = db.query(Proyecto).filter(Proyecto.nombre_organizacion == entity_id).all()
        cascade_info["proyectos"] = len(proyectos)
        
        # Contar actividades de esos proyectos
        actividades_count = 0
        localizaciones_count = 0
        participaciones_count = 0
        coordinaciones_count = 0
        recursos_usados_count = 0
        
        for proyecto in proyectos:
            actividades = db.query(Actividad).filter(
                Actividad.id_proyecto == proyecto.id_proyecto
            ).all()
            actividades_count += len(actividades)
            
            for actividad in actividades:
                localizaciones = db.query(Localizacion).filter(
                    Localizacion.id_actividad == actividad.id_actividad,
                    Localizacion.id_proyecto == proyecto.id_proyecto
                ).all()
                localizaciones_count += len(localizaciones)
                
                for loc in localizaciones:
                    participaciones_count += db.query(Participa).filter(
                        Participa.id_localizacion == loc.id_localizacion,
                        Participa.id_actividad == loc.id_actividad,
                        Participa.id_proyecto == loc.id_proyecto
                    ).count()
                    
                    coordinaciones_count += db.query(Coordina).filter(
                        Coordina.id_localizacion == loc.id_localizacion,
                        Coordina.id_actividad == loc.id_actividad,
                        Coordina.id_proyecto == loc.id_proyecto
                    ).count()
            
            recursos_usados_count += db.query(RecursoUsado).filter(
                RecursoUsado.id_proyecto == proyecto.id_proyecto
            ).count()
        
        cascade_info["actividades"] = actividades_count
        cascade_info["localizaciones"] = localizaciones_count
        cascade_info["participaciones"] = participaciones_count
        cascade_info["coordinaciones"] = coordinaciones_count
        cascade_info["recursos_usados"] = recursos_usados_count
        
        # Contar cesiones
        cascade_info["cesiones"] = db.query(Cesion).filter(
            Cesion.nombre_organizacion == entity_id
        ).count()
    
    elif entity_type == "proyecto":
        # Contar actividades
        actividades = db.query(Actividad).filter(
            Actividad.id_proyecto == entity_id
        ).all()
        cascade_info["actividades"] = len(actividades)
        
        # Contar localizaciones, participaciones y coordinaciones
        localizaciones_count = 0
        participaciones_count = 0
        coordinaciones_count = 0
        
        for actividad in actividades:
            localizaciones = db.query(Localizacion).filter(
                Localizacion.id_actividad == actividad.id_actividad,
                Localizacion.id_proyecto == entity_id
            ).all()
            localizaciones_count += len(localizaciones)
            
            for loc in localizaciones:
                participaciones_count += db.query(Participa).filter(
                    Participa.id_localizacion == loc.id_localizacion,
                    Participa.id_actividad == loc.id_actividad,
                    Participa.id_proyecto == loc.id_proyecto
                ).count()
                
                coordinaciones_count += db.query(Coordina).filter(
                    Coordina.id_localizacion == loc.id_localizacion,
                    Coordina.id_actividad == loc.id_actividad,
                    Coordina.id_proyecto == loc.id_proyecto
                ).count()
        
        cascade_info["localizaciones"] = localizaciones_count
        cascade_info["participaciones"] = participaciones_count
        cascade_info["coordinaciones"] = coordinaciones_count
        
        # Contar recursos usados y cesiones
        cascade_info["recursos_usados"] = db.query(RecursoUsado).filter(
            RecursoUsado.id_proyecto == entity_id
        ).count()
        
        cascade_info["cesiones"] = db.query(Cesion).filter(
            Cesion.id_proyecto == entity_id
        ).count()
    
    elif entity_type == "voluntario":
        # Contar skills
        cascade_info["skills"] = db.query(VoluntarioSkill).filter(
            VoluntarioSkill.dni_voluntario == entity_id
        ).count()
        
        # Contar participaciones, coordinaciones y cesiones
        cascade_info["participaciones"] = db.query(Participa).filter(
            Participa.dni_voluntario == entity_id
        ).count()
        
        cascade_info["coordinaciones"] = db.query(Coordina).filter(
            Coordina.dni_voluntario == entity_id
        ).count()
        
        cascade_info["cesiones"] = db.query(Cesion).filter(
            Cesion.dni_voluntario == entity_id
        ).count()
    
    elif entity_type == "actividad":
        # Contar localizaciones
        localizaciones = db.query(Localizacion).filter(
            Localizacion.id_actividad == entity_id
        ).all()
        cascade_info["localizaciones"] = len(localizaciones)
        
        # Contar participaciones y coordinaciones
        participaciones_count = 0
        coordinaciones_count = 0
        
        for loc in localizaciones:
            participaciones_count += db.query(Participa).filter(
                Participa.id_localizacion == loc.id_localizacion,
                Participa.id_actividad == loc.id_actividad,
                Participa.id_proyecto == loc.id_proyecto
            ).count()
            
            coordinaciones_count += db.query(Coordina).filter(
                Coordina.id_localizacion == loc.id_localizacion,
                Coordina.id_actividad == loc.id_actividad,
                Coordina.id_proyecto == loc.id_proyecto
            ).count()
        
        cascade_info["participaciones"] = participaciones_count
        cascade_info["coordinaciones"] = coordinaciones_count
    
    elif entity_type == "localizacion":
        # Para localización necesitamos los 3 IDs
        # Este caso se maneja de forma especial en el router
        pass
    
    return cascade_info
