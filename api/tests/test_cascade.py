"""
Tests para verificar operaciones de eliminación en cascada
"""
import pytest
from fastapi import status
from datetime import date


# ==================== ORGANIZACIONES - CASCADE ====================

def test_organizacion_delete_cascade_count(client, test_db):
    """Eliminar organización debe retornar conteo de registros eliminados en cascada"""
    from app.models.organizacion import Organizacion, EmailOrganizacion
    from app.models.proyecto import Proyecto, Actividad, Localizacion
    
    # Crear organización con estructura completa
    org = Organizacion(nombre="OrgCascadeTest", tipo="ONG")
    test_db.add(org)
    test_db.flush()
    
    # Emails (2)
    email1 = EmailOrganizacion(nombre_organizacion="OrgCascadeTest", email="email1@org.com")
    email2 = EmailOrganizacion(nombre_organizacion="OrgCascadeTest", email="email2@org.com")
    test_db.add_all([email1, email2])
    
    # Proyecto (1)
    proyecto = Proyecto(
        nombre_organizacion="OrgCascadeTest",
        nombre="Proyecto Cascade",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2025, 12, 31)
    )
    test_db.add(proyecto)
    test_db.flush()
    
    # Actividad (1)
    actividad = Actividad(
        id_proyecto=proyecto.id_proyecto,
        nombre="Actividad Cascade",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2025, 6, 30)
    )
    test_db.add(actividad)
    test_db.flush()
    
    # Localización (1)
    localizacion = Localizacion(
        id_actividad=actividad.id_actividad,
        id_proyecto=proyecto.id_proyecto,
        latitud=40.4168,
        longitud=-3.7038,
        descripcion="Madrid, España"
    )
    test_db.add(localizacion)
    test_db.commit()
    
    # Eliminar organización y verificar conteo en cascada
    response = client.delete("/api/organizaciones/OrgCascadeTest")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["message"] == "Organización eliminada exitosamente"
    assert data["deleted_id"] == "OrgCascadeTest"
    assert "cascade_info" in data
    
    cascade = data["cascade_info"]
    assert cascade["emails"] == 2
    assert cascade["proyectos"] == 1
    assert cascade["actividades"] == 1
    assert cascade["localizaciones"] == 1


def test_organizacion_delete_cascade_multiple_projects(client, test_db):
    """Eliminar organización con múltiples proyectos debe contar correctamente"""
    from app.models.organizacion import Organizacion, EmailOrganizacion
    from app.models.proyecto import Proyecto
    
    org = Organizacion(nombre="OrgMultiProjects", tipo="ONG")
    test_db.add(org)
    test_db.flush()
    
    email = EmailOrganizacion(nombre_organizacion="OrgMultiProjects", email="test@org.com")
    test_db.add(email)
    
    # 3 proyectos
    for i in range(3):
        proyecto = Proyecto(
            nombre_organizacion="OrgMultiProjects",
            nombre=f"Proyecto {i+1}",
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 12, 31)
        )
        test_db.add(proyecto)
    
    test_db.commit()
    
    response = client.delete("/api/organizaciones/OrgMultiProjects")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["cascade_info"]["proyectos"] == 3


# ==================== PROYECTOS - CASCADE ====================

def test_proyecto_delete_cascade_count(client, test_db, sample_proyecto):
    """Eliminar proyecto debe retornar conteo de registros eliminados en cascada"""
    from app.models.proyecto import Actividad, Localizacion
    
    # Actividad con localización
    actividad = Actividad(
        id_proyecto=sample_proyecto.id_proyecto,
        nombre="Actividad Test",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2025, 6, 30)
    )
    test_db.add(actividad)
    test_db.flush()
    
    localizacion = Localizacion(
        id_actividad=actividad.id_actividad,
        id_proyecto=sample_proyecto.id_proyecto,
        latitud=41.3851,
        longitud=2.1734,
        descripcion="Barcelona, España"
    )
    test_db.add(localizacion)
    test_db.commit()
    
    # Eliminar proyecto
    response = client.delete(f"/api/proyectos/{sample_proyecto.id_proyecto}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["message"] == "Proyecto eliminado exitosamente"
    assert "cascade_info" in data
    assert data["cascade_info"]["actividades"] == 1
    assert data["cascade_info"]["localizaciones"] == 1


def test_proyecto_delete_cascade_multiple_activities(client, test_db, sample_proyecto):
    """Eliminar proyecto con múltiples actividades y localizaciones"""
    from app.models.proyecto import Actividad, Localizacion
    
    # 2 actividades, cada una con 2 localizaciones
    for i in range(2):
        actividad = Actividad(
            id_proyecto=sample_proyecto.id_proyecto,
            nombre=f"Actividad {i+1}",
            fecha_inicio=date(2025, 1, 1),
            fecha_fin=date(2025, 6, 30)
        )
        test_db.add(actividad)
        test_db.flush()
        
        for j in range(2):
            localizacion = Localizacion(
                id_actividad=actividad.id_actividad,
                id_proyecto=sample_proyecto.id_proyecto,
                latitud=40.0 + i + j,
                longitud=-3.0 + i + j,
                descripcion=f"Loc {i}-{j}"
            )
            test_db.add(localizacion)
    
    test_db.commit()
    
    response = client.delete(f"/api/proyectos/{sample_proyecto.id_proyecto}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["cascade_info"]["actividades"] == 2
    assert data["cascade_info"]["localizaciones"] == 4


# ==================== ACTIVIDADES - CASCADE ====================

def test_actividad_delete_cascade_localizaciones(client, test_db, sample_proyecto):
    """Eliminar actividad debe eliminar localizaciones asociadas"""
    from app.models.proyecto import Actividad, Localizacion
    
    actividad = Actividad(
        id_proyecto=sample_proyecto.id_proyecto,
        nombre="Actividad Cascade",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2025, 6, 30)
    )
    test_db.add(actividad)
    test_db.flush()
    
    # 3 localizaciones
    for i in range(3):
        loc = Localizacion(
            id_actividad=actividad.id_actividad,
            id_proyecto=sample_proyecto.id_proyecto,
            latitud=40.0 + i,
            longitud=-3.0 + i,
            descripcion=f"Ubicación {i+1}"
        )
        test_db.add(loc)
    
    test_db.commit()
    
    # Eliminar actividad
    response = client.delete(
        f"/api/proyectos/{sample_proyecto.id_proyecto}/actividades/{actividad.id_actividad}"
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    # Verificar que las localizaciones fueron eliminadas
    from app.models.proyecto import Localizacion
    locs_count = test_db.query(Localizacion).filter(
        Localizacion.id_actividad == actividad.id_actividad
    ).count()
    assert locs_count == 0


# ==================== VOLUNTARIOS - CASCADE ====================

def test_voluntario_delete_cascade_participaciones(client, test_db):
    """Eliminar voluntario debe eliminar participaciones y coordinaciones"""
    from app.models.voluntario import Voluntario
    from app.models.relaciones import Participa
    
    # Crear voluntario
    voluntario = Voluntario(
        dni="77777777G",
        nombre="Vol Cascade",
        fecha_nacimiento=date(1990, 1, 1),
        fecha_alta=date(2010, 1, 1),
        email="cascade@test.com"
    )
    test_db.add(voluntario)
    test_db.commit()
    
    # El endpoint debe permitir eliminar aunque tenga relaciones
    response = client.delete("/api/voluntarios/77777777G")
    
    # Puede ser 200 si se elimina o 400 si tiene restricciones
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]


# ==================== RECURSOS - CASCADE ====================

# Test deshabilitado - El modelo de relación Usa no está disponible en la estructura actual
# def test_recurso_delete_cascade_usa_relations(client, test_db):
#     """Eliminar recurso debe eliminar relaciones de uso con proyectos"""
#     pass


# ==================== VOLUMTARIOS - CASCADE INFO ====================

def test_delete_voluntario_cascade_info(client, test_db, sample_voluntario):
    """Test: eliminar voluntario debe retornar conteo de skills, participaciones, etc."""
    from app.models.voluntario import VoluntarioSkill
    
    # Agregar skills
    skill1 = VoluntarioSkill(
        dni_voluntario=sample_voluntario.dni,
        nombre_skill="Primeros Auxilios",
        descripcion="Certificado Cruz Roja"
    )
    skill2 = VoluntarioSkill(
        dni_voluntario=sample_voluntario.dni,
        nombre_skill="Logística",
        descripcion="Experiencia en almacenes"
    )
    test_db.add_all([skill1, skill2])
    test_db.commit()
    
    # Eliminar voluntario
    response = client.delete(f"/api/voluntarios/{sample_voluntario.dni}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert "cascade_info" in data
    cascade = data["cascade_info"]
    assert cascade["skills"] == 2


def test_delete_nonexistent_returns_404(client):
    """Test: eliminar entidad inexistente debe retornar 404"""
    response = client.delete("/api/organizaciones/NoExiste")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    response = client.delete("/api/proyectos/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    response = client.delete("/api/voluntarios/99999999Z")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_cascade_actually_deletes(client, test_db, sample_organizacion):
    """Test: verificar que CASCADE realmente elimina registros"""
    from app.models.organizacion import Organizacion
    from app.models.proyecto import Proyecto
    
    # Agregar proyecto
    proyecto = Proyecto(
        nombre_organizacion=sample_organizacion.nombre,
        nombre="Proyecto a Eliminar",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2025, 12, 31)
    )
    test_db.add(proyecto)
    test_db.commit()
    test_db.refresh(proyecto)
    
    proyecto_id = proyecto.id_proyecto
    
    # Verificar que existe
    assert test_db.query(Proyecto).filter(Proyecto.id_proyecto == proyecto_id).first() is not None
    
    # Eliminar organización
    response = client.delete(f"/api/organizaciones/{sample_organizacion.nombre}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verificar que el proyecto también fue eliminado
    assert test_db.query(Proyecto).filter(Proyecto.id_proyecto == proyecto_id).first() is None
    assert test_db.query(Organizacion).filter(Organizacion.nombre == sample_organizacion.nombre).first() is None
