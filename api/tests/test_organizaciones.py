"""
Tests para endpoints de Organizaciones
"""
import pytest
from fastapi import status


# ==================== CREATE ====================

def test_organizacion_create_success(client):
    """Crear organización con datos válidos"""
    response = client.post("/api/organizaciones", json={
        "nombre": "Cruz Roja Test",
        "tipo": "Humanitaria",
        "emails": ["info@cruzroja.com", "contacto@cruzroja.com"]
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nombre"] == "Cruz Roja Test"
    assert data["tipo"] == "Humanitaria"
    assert len(data["emails"]) == 2


def test_organizacion_create_duplicate(client):
    """Crear organización con nombre duplicado debe fallar"""
    client.post("/api/organizaciones", json={
        "nombre": "ONG Duplicada",
        "tipo": "ONG",
        "emails": ["test@ong.com"]
    })
    
    response = client.post("/api/organizaciones", json={
        "nombre": "ONG Duplicada",
        "tipo": "ONG",
        "emails": ["otro@ong.com"]
    })
    
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT]


# ==================== READ ====================

def test_organizacion_list_with_pagination(client):
    """Listar organizaciones con paginación"""
    response = client.get("/api/organizaciones?skip=0&limit=10")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


def test_organizacion_get_by_name_success(client):
    """Obtener organización existente por nombre"""
    client.post("/api/organizaciones", json={
        "nombre": "Médicos Sin Fronteras",
        "tipo": "Médica",
        "emails": ["info@msf.com"]
    })
    
    response = client.get("/api/organizaciones/Médicos%20Sin%20Fronteras")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nombre"] == "Médicos Sin Fronteras"
    assert data["tipo"] == "Médica"


def test_organizacion_get_by_name_not_found(client):
    """Obtener organización inexistente debe retornar 404"""
    response = client.get("/api/organizaciones/NoExiste")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ==================== UPDATE ====================

def test_organizacion_update_success(client):
    """Actualizar organización existente"""
    client.post("/api/organizaciones", json={
        "nombre": "ONG Update",
        "tipo": "Humanitaria",
        "emails": ["original@test.com"]
    })
    
    response = client.put("/api/organizaciones/ONG%20Update", json={
        "tipo": "Educativa"
    })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["tipo"] == "Educativa"


def test_organizacion_update_not_found(client):
    """Actualizar organización inexistente debe fallar"""
    response = client.put("/api/organizaciones/NoExiste", json={
        "tipo": "Educativa"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ==================== DELETE ====================

def test_organizacion_delete_success(client):
    """Eliminar organización sin dependencias"""
    client.post("/api/organizaciones", json={
        "nombre": "ONG Delete",
        "tipo": "ONG",
        "emails": ["delete@test.com"]
    })
    
    response = client.delete("/api/organizaciones/ONG%20Delete")
    assert response.status_code == status.HTTP_200_OK


def test_organizacion_delete_not_found(client):
    """Eliminar organización inexistente debe retornar 404"""
    response = client.delete("/api/organizaciones/NoExiste")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ==================== EMAILS ====================

def test_organizacion_email_delete_success(client):
    """Eliminar email de organización"""
    client.post("/api/organizaciones", json={
        "nombre": "ONG Email",
        "tipo": "ONG",
        "emails": ["email1@test.com", "email2@test.com"]
    })
    
    response = client.delete("/api/organizaciones/ONG%20Email/emails/email1@test.com")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_organizacion_email_delete_not_found_org(client):
    """Eliminar email de organización inexistente"""
    response = client.delete("/api/organizaciones/NoExiste/emails/test@test.com")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_organizacion_email_delete_not_found_email(client):
    """Eliminar email inexistente de organización existente"""
    client.post("/api/organizaciones", json={
        "nombre": "ONG Email Test",
        "tipo": "ONG",
        "emails": ["email1@test.com"]
    })
    
    response = client.delete("/api/organizaciones/ONG%20Email%20Test/emails/noexiste@test.com")
    assert response.status_code == status.HTTP_404_NOT_FOUND
