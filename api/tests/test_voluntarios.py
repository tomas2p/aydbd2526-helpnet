"""
Tests para endpoints de Voluntarios y Skills
"""
import pytest
from datetime import date, timedelta
from fastapi import status


# ==================== VOLUNTARIOS - CREATE ====================

def test_voluntario_create_success_age_valid(client):
    """Crear voluntario con edad válida (18+ años)"""
    fecha_nacimiento = date(2000, 1, 1)
    fecha_alta = date(2020, 1, 1)
    
    response = client.post("/api/voluntarios", json={
        "dni": "11111111A",
        "nombre": "Juan",
        "apellido1": "Pérez",
        "fecha_nacimiento": str(fecha_nacimiento),
        "fecha_alta": str(fecha_alta),
        "email": "juan@test.com",
        "skills": []
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["dni"] == "11111111A"
    assert data["nombre"] == "Juan"


def test_voluntario_create_fails_under_18(client):
    """Crear voluntario menor de 18 años debe fallar"""
    fecha_nacimiento = date(2010, 1, 1)
    fecha_alta = date(2020, 1, 1)
    
    response = client.post("/api/voluntarios", json={
        "dni": "22222222B",
        "nombre": "Menor",
        "fecha_nacimiento": str(fecha_nacimiento),
        "fecha_alta": str(fecha_alta),
        "email": "menor@test.com"
    })
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    error_detail = response.json().get("detail", [])
    if isinstance(error_detail, list) and len(error_detail) > 0:
        error_msg = error_detail[0].get("msg", "")
        assert "18 años" in error_msg
    else:
        assert "18 años" in str(error_detail)


def test_voluntario_create_exactly_18_years(client):
    """Crear voluntario con exactamente 18 años debe ser aceptado"""
    hoy = date.today()
    fecha_nacimiento = hoy - timedelta(days=18*365 + 5)
    fecha_alta = hoy
    
    response = client.post("/api/voluntarios", json={
        "dni": "33333333C",
        "nombre": "Voluntario",
        "fecha_nacimiento": str(fecha_nacimiento),
        "fecha_alta": str(fecha_alta),
        "email": "18@test.com"
    })
    
    assert response.status_code == status.HTTP_201_CREATED


def test_voluntario_create_fails_fecha_alta_before_birth(client):
    """Fecha alta anterior al nacimiento debe fallar"""
    response = client.post("/api/voluntarios", json={
        "dni": "44444444D",
        "nombre": "Imposible",
        "fecha_nacimiento": "2010-01-01",
        "fecha_alta": "2000-01-01",
        "email": "imposible@test.com"
    })
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_voluntario_create_duplicate_dni_fails(client, sample_voluntario):
    """Crear voluntario con DNI duplicado debe fallar"""
    response = client.post("/api/voluntarios", json={
        "dni": sample_voluntario.dni,
        "nombre": "Otro Nombre",
        "fecha_nacimiento": "1990-01-01",
        "fecha_alta": "2020-01-01",
        "email": "otro@test.com"
    })
    
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT]


# ==================== VOLUNTARIOS - READ ====================

def test_voluntario_list_with_pagination(client):
    """Listar voluntarios con paginación"""
    response = client.get("/api/voluntarios?skip=0&limit=10")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_voluntario_get_by_dni_success(client, sample_voluntario):
    """Obtener voluntario existente por DNI"""
    response = client.get(f"/api/voluntarios/{sample_voluntario.dni}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["dni"] == sample_voluntario.dni


def test_voluntario_get_by_dni_not_found(client):
    """Obtener voluntario inexistente debe retornar 404"""
    response = client.get("/api/voluntarios/00000000X")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_voluntario_get_edad_calculated(client, sample_voluntario):
    """Obtener edad calculada de voluntario"""
    response = client.get(f"/api/voluntarios/{sample_voluntario.dni}/edad")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "edad" in data
    assert data["edad"] >= 18


# ==================== VOLUNTARIOS - UPDATE ====================

def test_voluntario_update_success(client, sample_voluntario):
    """Actualizar datos de voluntario"""
    response = client.put(f"/api/voluntarios/{sample_voluntario.dni}", json={
        "email": "nuevo@email.com"
    })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "nuevo@email.com"


def test_voluntario_update_not_found(client):
    """Actualizar voluntario inexistente debe fallar"""
    response = client.put("/api/voluntarios/00000000X", json={
        "email": "test@test.com"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ==================== VOLUNTARIOS - DELETE ====================

def test_voluntario_delete_success(client):
    """Eliminar voluntario sin dependencias"""
    client.post("/api/voluntarios", json={
        "dni": "55555555E",
        "nombre": "Delete",
        "fecha_nacimiento": "1990-01-01",
        "fecha_alta": "2010-01-01",
        "email": "delete@test.com"
    })
    
    response = client.delete("/api/voluntarios/55555555E")
    assert response.status_code == status.HTTP_200_OK


# ==================== SKILLS - CREATE ====================

def test_skill_add_to_voluntario_success(client, sample_voluntario):
    """Agregar skill a voluntario existente"""
    response = client.post(f"/api/voluntarios/{sample_voluntario.dni}/skills", json={
        "nombre_skill": "FastAPI",
        "descripcion": "Framework web avanzado"
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nombre_skill"] == "FastAPI"
    assert data["descripcion"] == "Framework web avanzado"


def test_skill_add_voluntario_not_found(client):
    """Agregar skill a voluntario inexistente debe fallar"""
    response = client.post("/api/voluntarios/00000000X/skills", json={
        "nombre_skill": "Python",
        "descripcion": "Lenguaje de programación"
    })
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ==================== SKILLS - READ ====================

def test_skill_list_by_voluntario(client, sample_voluntario):
    """Listar skills de un voluntario"""
    response = client.get(f"/api/voluntarios/{sample_voluntario.dni}/skills")
    
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_skill_list_voluntario_not_found(client):
    """Listar skills de voluntario inexistente debe fallar"""
    response = client.get("/api/voluntarios/00000000X/skills")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ==================== SKILLS - DELETE ====================

def test_skill_delete_success(client):
    """Eliminar skill de voluntario"""
    vol_resp = client.post("/api/voluntarios", json={
        "dni": "66666666F",
        "nombre": "Test Skills",
        "fecha_nacimiento": "1985-01-01",
        "fecha_alta": "2005-01-01",
        "email": "skills@test.com",
        "skills": []
    })
    assert vol_resp.status_code == status.HTTP_201_CREATED
    
    client.post("/api/voluntarios/66666666F/skills", json={
        "nombre_skill": "Django",
        "descripcion": "Framework web"
    })
    
    response = client.delete("/api/voluntarios/66666666F/skills/Django")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_skill_delete_not_found(client, sample_voluntario):
    """Eliminar skill inexistente debe fallar"""
    response = client.delete(f"/api/voluntarios/{sample_voluntario.dni}/skills/NoExiste")
    assert response.status_code == status.HTTP_404_NOT_FOUND

