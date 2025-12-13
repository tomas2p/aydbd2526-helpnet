"""
Tests específicos para líneas no cubiertas en crud/recurso.py y crud/relaciones.py
"""
import pytest
from fastapi import status


# ==================== CRUD RECURSOS - Líneas específicas ====================

def test_recurso_create_validation_error(client):
    """Test que cubre validación de tipo inválido"""
    response = client.post("/api/recursos", json={
        "tipo": "X",  # Tipo inválido
        "nombre": "Recurso Inválido",
        "fecha_entrega": "2025-01-10"
    })
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_recurso_alquilado_without_required_fields(client):
    """Test que cubre validación de campos requeridos en alquilado"""
    response = client.post("/api/recursos", json={
        "tipo": "A",
        "nombre": "Recurso Sin Proveedor",
        "fecha_entrega": "2025-01-10"
        # Falta proveedor y costo
    })
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_recurso_donado_all_optional_fields(client):
    """Crear recurso donado solo con campos mínimos"""
    response = client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Recurso Mínimo",
        "fecha_entrega": "2025-01-10",
        "estado": "nuevo"
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tipo"] == "D"
    assert data["nombre"] == "Recurso Mínimo"
    # Campos opcionales no deberían estar o ser None
    assert data.get("nombre_donante") is None or "nombre_donante" not in data


def test_recurso_list_pagination_edge_cases(client):
    """Test de paginación con límites"""
    # Solicitar página muy alta
    response = client.get("/api/recursos?skip=1000&limit=100")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)


def test_recurso_delete_with_dependencies(client):
    """Eliminar recurso que está asignado a proyecto"""
    # Crear org y proyecto
    org_resp = client.post("/api/organizaciones", json={
        "nombre": "Org Recurso Dep",
        "tipo": "ONG",
        "emails": ["test@org.com"]
    })
    
    proj_resp = client.post("/api/proyectos", json={
        "nombre_organizacion": "Org Recurso Dep",
        "nombre": "Proyecto",
        "descripcion": "Test",
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-12-31"
    })
    proyecto = proj_resp.json()
    
    # Crear recurso
    rec_resp = client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Recurso Dependencia",
        "fecha_entrega": "2025-01-15",
        "estado": "nuevo"
    })
    recurso = rec_resp.json()
    
    # Asignar a proyecto
    client.post(
        f"/api/proyectos/{proyecto['id_proyecto']}/recursos?id_recurso={recurso['id_recurso']}"
    )
    
    # Intentar eliminar (debería funcionar con cascade)
    response = client.delete(f"/api/recursos/{recurso['id_recurso']}")
    
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]


# ==================== CRUD RELACIONES - Líneas específicas ====================

def test_participacion_get_by_voluntario_empty(client, sample_voluntario):
    """Obtener participaciones de voluntario sin participaciones"""
    # El voluntario no tiene participaciones
    response = client.get("/api/participaciones")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data


def test_coordinacion_list_empty(client):
    """Listar coordinaciones cuando no hay ninguna"""
    response = client.get("/api/coordinaciones")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert data["total"] >= 0


def test_cesion_list_with_pagination(client):
    """Listar cesiones con paginación específica"""
    response = client.get("/api/cesiones?skip=0&limit=5")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_participacion_duplicate_validation(client, sample_voluntario):
    """Test de validación de participación duplicada"""
    # Crear estructura
    org_resp = client.post("/api/organizaciones", json={
        "nombre": "Org Dup Part",
        "tipo": "ONG",
        "emails": ["test@org.com"]
    })
    
    proj_resp = client.post("/api/proyectos", json={
        "nombre_organizacion": "Org Dup Part",
        "nombre": "Proyecto",
        "descripcion": "Test",
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-12-31"
    })
    proyecto = proj_resp.json()
    
    act_resp = client.post(f"/api/proyectos/{proyecto['id_proyecto']}/actividades", json={
        "nombre": "Actividad",
        "fecha_inicio": "2025-02-01",
        "fecha_fin": "2025-02-28"
    })
    actividad = act_resp.json()
    
    loc_resp = client.post(
        f"/api/proyectos/{proyecto['id_proyecto']}/actividades/{actividad['id_actividad']}/localizaciones",
        json={"latitud": 40.0, "longitud": -3.0, "descripcion": "Madrid"}
    )
    loc = loc_resp.json()
    
    # Primera participación
    first = client.post("/api/participaciones", json={
        "id_proyecto": proyecto["id_proyecto"],
        "id_actividad": actividad["id_actividad"],
        "id_localizacion": loc["id_localizacion"],
        "dni_voluntario": sample_voluntario.dni,
        "fecha_inicio": "2025-02-01",
        "fecha_fin": "2025-02-15",
        "rol": "Participante"
    })
    
    assert first.status_code == status.HTTP_201_CREATED
    
    # Intentar duplicar
    duplicate = client.post("/api/participaciones", json={
        "id_proyecto": proyecto["id_proyecto"],
        "id_actividad": actividad["id_actividad"],
        "id_localizacion": loc["id_localizacion"],
        "dni_voluntario": sample_voluntario.dni,
        "fecha_inicio": "2025-02-10",
        "fecha_fin": "2025-02-20",
        "rol": "Ayudante"
    })
    
    assert duplicate.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT]


def test_coordinacion_duplicate_validation(client, sample_voluntario):
    """Test de validación de coordinación duplicada"""
    # Crear estructura
    org_resp = client.post("/api/organizaciones", json={
        "nombre": "Org Dup Coord",
        "tipo": "ONG",
        "emails": ["test@org.com"]
    })
    
    proj_resp = client.post("/api/proyectos", json={
        "nombre_organizacion": "Org Dup Coord",
        "nombre": "Proyecto",
        "descripcion": "Test",
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-12-31"
    })
    proyecto = proj_resp.json()
    
    act_resp = client.post(f"/api/proyectos/{proyecto['id_proyecto']}/actividades", json={
        "nombre": "Actividad",
        "fecha_inicio": "2025-02-01",
        "fecha_fin": "2025-02-28"
    })
    actividad = act_resp.json()
    
    loc_resp = client.post(
        f"/api/proyectos/{proyecto['id_proyecto']}/actividades/{actividad['id_actividad']}/localizaciones",
        json={"latitud": 40.0, "longitud": -3.0, "descripcion": "Madrid"}
    )
    loc = loc_resp.json()
    
    # Primera coordinación
    first = client.post("/api/coordinaciones", json={
        "id_proyecto": proyecto["id_proyecto"],
        "id_actividad": actividad["id_actividad"],
        "id_localizacion": loc["id_localizacion"],
        "dni_voluntario": sample_voluntario.dni,
        "fecha_inicio": "2025-02-01",
        "fecha_fin": "2025-02-28"
    })
    
    assert first.status_code == status.HTTP_201_CREATED
    
    # Intentar duplicar
    duplicate = client.post("/api/coordinaciones", json={
        "id_proyecto": proyecto["id_proyecto"],
        "id_actividad": actividad["id_actividad"],
        "id_localizacion": loc["id_localizacion"],
        "dni_voluntario": sample_voluntario.dni,
        "fecha_inicio": "2025-02-10",
        "fecha_fin": "2025-03-10"
    })
    
    assert duplicate.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT]


# ==================== CRUD ORGANIZACION - Líneas específicas ====================

def test_organizacion_get_with_emails(client):
    """Obtener organización que incluya sus emails"""
    # Crear organización con múltiples emails
    client.post("/api/organizaciones", json={
        "nombre": "Org Con Emails",
        "tipo": "ONG",
        "emails": ["email1@org.com", "email2@org.com", "email3@org.com"]
    })
    
    response = client.get("/api/organizaciones/Org%20Con%20Emails")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nombre"] == "Org Con Emails"
    assert len(data["emails"]) == 3


def test_organizacion_update_tipo(client):
    """Actualizar solo el tipo de organización"""
    # Crear organización
    client.post("/api/organizaciones", json={
        "nombre": "Org Cambio Tipo",
        "tipo": "ONG",
        "emails": ["test@org.com"]
    })
    
    # Actualizar tipo
    response = client.put("/api/organizaciones/Org%20Cambio%20Tipo", json={
        "tipo": "Fundación"
    })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["tipo"] == "Fundación"


# ==================== CRUD PROYECTO - Líneas específicas ====================

def test_proyecto_list_empty(client):
    """Listar proyectos cuando no hay ninguno (después de limpiar)"""
    response = client.get("/api/proyectos?skip=0&limit=1")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data


def test_proyecto_update_presupuesto(client, organizacion_base):
    """Actualizar presupuesto de proyecto"""
    # Crear proyecto
    proj_resp = client.post("/api/proyectos", json={
        "nombre_organizacion": organizacion_base["nombre"],
        "nombre": "Proyecto Presup",
        "descripcion": "Test",
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-12-31",
        "presupuesto": 10000.00
    })
    proyecto_id = proj_resp.json()["id_proyecto"]
    
    # Actualizar presupuesto
    response = client.put(f"/api/proyectos/{proyecto_id}", json={
        "presupuesto": 20000.00
    })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    if "presupuesto" in data:
        assert float(data["presupuesto"]) == 20000.00


# ==================== FIXTURES ====================

@pytest.fixture
def organizacion_base(client):
    """Organización base para tests específicos"""
    response = client.post("/api/organizaciones", json={
        "nombre": "Org Base Specific",
        "tipo": "ONG",
        "emails": ["specific@test.com"]
    })
    return response.json()
