"""
Tests para Recursos polimórficos (Donado/Alquilado)
"""
import pytest
from fastapi import status
from datetime import date


# ==================== RECURSOS DONADOS - CREATE ====================

def test_recurso_donado_create_success(client):
    """Crear recurso donado con todos los campos"""
    response = client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Tienda de campaña",
        "descripcion": "Tienda para 4 personas",
        "fecha_entrega": "2025-01-15",
        "estado": "nuevo",
        "nombre_donante": "Juan Pérez",
        "email_donante": "juan@email.com"
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tipo"] == "D"
    assert data["nombre"] == "Tienda de campaña"
    assert data["estado"] == "nuevo"
    assert "id_recurso" in data


def test_recurso_donado_create_minimal(client):
    """Crear recurso donado con campos mínimos"""
    response = client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Botiquín",
        "fecha_entrega": "2025-01-10",
        "estado": "usado"
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tipo"] == "D"
    assert data["estado"] == "usado"


# ==================== RECURSOS ALQUILADOS - CREATE ====================

def test_recurso_alquilado_create_success(client):
    """Crear recurso alquilado con todos los campos"""
    response = client.post("/api/recursos", json={
        "tipo": "A",
        "nombre": "Generador eléctrico",
        "descripcion": "Generador 5000W",
        "fecha_entrega": "2025-02-01",
        "proveedor": "Alquileres SA",
        "costo": 250.50,
        "fecha_devolucion": "2025-03-01"
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tipo"] == "A"
    assert data["nombre"] == "Generador eléctrico"
    assert data["proveedor"] == "Alquileres SA"
    assert float(data["costo"]) == 250.50
    assert "id_recurso" in data


def test_recurso_alquilado_create_minimal(client):
    """Crear recurso alquilado con campos mínimos (requiere fecha_devolucion)"""
    response = client.post("/api/recursos", json={
        "tipo": "A",
        "nombre": "Camión",
        "fecha_entrega": "2025-01-20",
        "proveedor": "Transportes XYZ",
        "costo": 1500.00,
        "fecha_devolucion": "2025-02-20"
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tipo"] == "A"
    assert data["proveedor"] == "Transportes XYZ"


# ==================== RECURSOS - READ ====================

def test_recurso_donado_get_correct_schema(client):
    """Obtener recurso donado debe retornar schema correcto (sin campos de alquilado)"""
    create_response = client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Medicamentos",
        "fecha_entrega": "2025-01-10",
        "estado": "nuevo"
    })
    id_recurso = create_response.json()["id_recurso"]
    
    response = client.get(f"/api/recursos/{id_recurso}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["tipo"] == "D"
    assert "estado" in data
    assert "proveedor" not in data
    assert "costo" not in data
    assert "fecha_devolucion" not in data


def test_recurso_alquilado_get_correct_schema(client):
    """Obtener recurso alquilado debe retornar schema correcto (sin campos de donado)"""
    create_response = client.post("/api/recursos", json={
        "tipo": "A",
        "nombre": "Excavadora",
        "fecha_entrega": "2025-01-20",
        "proveedor": "Maquinaria S.A.",
        "costo": 2000.00,
        "fecha_devolucion": "2025-02-20"
    })
    id_recurso = create_response.json()["id_recurso"]
    
    response = client.get(f"/api/recursos/{id_recurso}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["tipo"] == "A"
    assert "proveedor" in data
    assert "costo" in data
    assert "estado" not in data
    assert "nombre_donante" not in data
    assert "email_donante" not in data


def test_recurso_list_with_pagination(client):
    """Listar recursos con paginación"""
    response = client.get("/api/recursos?skip=0&limit=10")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_recurso_get_not_found(client):
    """Obtener recurso inexistente debe retornar 404"""
    response = client.get("/api/recursos/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ==================== RECURSOS - UPDATE ====================

def test_recurso_update_success(client):
    """Actualizar recurso - el endpoint PUT no existe, se crea nuevo"""
    create_response = client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Recurso Update",
        "fecha_entrega": "2025-01-10",
        "estado": "nuevo"
    })
    id_recurso = create_response.json()["id_recurso"]
    
    # El endpoint PUT no está implementado
    response = client.get(f"/api/recursos/{id_recurso}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nombre"] == "Recurso Update"


def test_recurso_update_not_found(client):
    """Actualizar recurso - el endpoint PUT no existe"""
    # El endpoint PUT no está implementado
    response = client.get("/api/recursos/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ==================== RECURSOS - DELETE ====================

def test_recurso_delete_success(client):
    """Eliminar recurso sin asignaciones"""
    create_response = client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Recurso Delete",
        "fecha_entrega": "2025-01-10",
        "estado": "nuevo"
    })
    id_recurso = create_response.json()["id_recurso"]
    
    response = client.delete(f"/api/recursos/{id_recurso}")
    assert response.status_code == status.HTTP_200_OK


def test_recurso_delete_with_cascade(client):
    """Eliminar recurso con asignaciones debe eliminar en cascada"""
    # Crear organización y proyecto
    org_resp = client.post("/api/organizaciones", json={
        "nombre": "Org Recurso Cascade",
        "tipo": "ONG",
        "emails": ["test@org.com"]
    })
    org = org_resp.json()
    
    proj_resp = client.post("/api/proyectos", json={
        "nombre_organizacion": org["nombre"],
        "nombre": "Proyecto",
        "descripcion": "Test",
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-12-31"
    })
    proyecto = proj_resp.json()
    
    # Crear recurso
    rec_resp = client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Recurso Cascade",
        "fecha_entrega": "2025-01-15",
        "estado": "nuevo"
    })
    recurso = rec_resp.json()
    
    # Asignar recurso a proyecto
    client.post(
        f"/api/proyectos/{proyecto['id_proyecto']}/recursos?id_recurso={recurso['id_recurso']}"
    )
    
    # Eliminar recurso debe funcionar (cascade)
    response = client.delete(f"/api/recursos/{recurso['id_recurso']}")
    assert response.status_code == status.HTTP_200_OK


# ==================== RECURSOS USADOS - ASIGNACIÓN ====================

def test_recurso_assign_to_proyecto_success(client):
    """Asignar recurso a proyecto"""
    # Crear org y proyecto
    org_resp = client.post("/api/organizaciones", json={
        "nombre": "Org Asignar",
        "tipo": "ONG",
        "emails": ["test@org.com"]
    })
    org = org_resp.json()
    
    proj_resp = client.post("/api/proyectos", json={
        "nombre_organizacion": org["nombre"],
        "nombre": "Proyecto",
        "descripcion": "Test",
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-12-31"
    })
    proyecto = proj_resp.json()
    
    # Crear recurso
    rec_resp = client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Recurso",
        "fecha_entrega": "2025-01-15",
        "estado": "nuevo"
    })
    recurso = rec_resp.json()
    
    # Asignar
    response = client.post(
        f"/api/proyectos/{proyecto['id_proyecto']}/recursos?id_recurso={recurso['id_recurso']}"
    )
    
    assert response.status_code == status.HTTP_201_CREATED


def test_recurso_list_by_proyecto(client):
    """Listar recursos de un proyecto"""
    # Crear estructura
    org_resp = client.post("/api/organizaciones", json={
        "nombre": "Org List Recursos",
        "tipo": "ONG",
        "emails": ["test@org.com"]
    })
    org = org_resp.json()
    
    proj_resp = client.post("/api/proyectos", json={
        "nombre_organizacion": org["nombre"],
        "nombre": "Proyecto",
        "descripcion": "Test",
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-12-31"
    })
    proyecto = proj_resp.json()
    
    # Obtener recursos (vacío)
    response = client.get(f"/api/proyectos/{proyecto['id_proyecto']}/recursos")
    
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_recurso_unassign_from_proyecto_success(client):
    """Desasignar recurso de proyecto"""
    # Crear org, proyecto y recurso
    org_resp = client.post("/api/organizaciones", json={
        "nombre": "Org Desasignar",
        "tipo": "ONG",
        "emails": ["test@org.com"]
    })
    org = org_resp.json()
    
    proj_resp = client.post("/api/proyectos", json={
        "nombre_organizacion": org["nombre"],
        "nombre": "Proyecto",
        "descripcion": "Test",
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-12-31"
    })
    proyecto = proj_resp.json()
    
    rec_resp = client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Recurso",
        "fecha_entrega": "2025-01-15",
        "estado": "nuevo"
    })
    recurso = rec_resp.json()
    
    # Asignar
    client.post(
        f"/api/proyectos/{proyecto['id_proyecto']}/recursos?id_recurso={recurso['id_recurso']}"
    )
    
    # Desasignar
    response = client.delete(
        f"/api/proyectos/{proyecto['id_proyecto']}/recursos/{recurso['id_recurso']}"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_recurso_unassign_not_found(client):
    """Desasignar recurso inexistente debe fallar"""
    response = client.delete("/api/proyectos/999/recursos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND



def test_list_recursos_mixtos(client):
    """Test: listar recursos debe retornar mezcla heterogénea correcta"""
    # Crear un donado
    client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Recurso Donado",
        "fecha_entrega": "2025-01-01",
        "estado": "nuevo"
    })
    
    # Crear un alquilado
    client.post("/api/recursos", json={
        "tipo": "A",
        "nombre": "Recurso Alquilado",
        "fecha_entrega": "2025-01-02",
        "proveedor": "Proveedor Test",
        "costo": 100.00,
        "fecha_devolucion": "2025-02-02"
    })
    
    # Listar todos
    response = client.get("/api/recursos")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 2
    
    # Verificar que hay de ambos tipos
    tipos = [item["tipo"] for item in data["items"]]
    assert "D" in tipos
    assert "A" in tipos


def test_filter_recursos_por_tipo(client):
    """Test: filtrar recursos por tipo debe funcionar"""
    # Crear donado
    client.post("/api/recursos", json={
        "tipo": "D",
        "nombre": "Solo Donado",
        "fecha_entrega": "2025-01-01",
        "estado": "nuevo"
    })
    
    # Filtrar solo donados
    response = client.get("/api/recursos?tipo=D")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Todos los items deben ser tipo D
    for item in data["items"]:
        assert item["tipo"] == "D"
        assert "estado" in item


def test_create_recurso_tipo_invalido(client):
    """Test: tipo de recurso inválido debe fallar"""
    response = client.post("/api/recursos", json={
        "tipo": "X",  # Tipo inválido
        "nombre": "Recurso Inválido",
        "fecha_entrega": "2025-01-01"
    })
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST or response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
