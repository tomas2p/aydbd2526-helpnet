"""
Configuración de fixtures y setup para tests con pytest

Este archivo contiene:
- Configuración de base de datos de prueba
- Cliente FastAPI para testing
- Fixtures reutilizables para entidades comunes (organizaciones, proyectos, voluntarios, recursos)

Estructura de fixtures:
    - test_engine: Engine de base de datos para toda la sesión de tests
    - test_db: Sesión de BD con rollback automático por cada test
    - client: Cliente HTTP de FastAPI con BD de prueba
    - sample_*: Fixtures de datos de ejemplo para tests
"""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar la aplicación y modelos
from app.main import app
from app.database import Base, get_database_url
from app.dependencies import get_db

# URL de base de datos de testing
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL_TEST",
    "postgresql://usuario:password@localhost:5432/helpnet_test"
)


# ==================== DATABASE SETUP ====================

@pytest.fixture(scope="session")
def test_engine():
    """
    Crea engine de base de datos para toda la sesión de tests.
    Las tablas se crean al inicio y se eliminan al final.
    """
    engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Limpiar al finalizar todos los tests
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(test_engine):
    """
    Crea una nueva sesión de BD para cada test con rollback automático.
    Esto asegura que cada test sea independiente y no afecte a otros.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestSessionLocal()
    
    yield session

    if transaction.is_active:
        transaction.rollback()
    session.close()
    connection.close()


@pytest.fixture(scope="function")
def client(test_db):
    """
    Cliente HTTP de FastAPI configurado con base de datos de prueba.
    Los endpoints usarán la BD de test en lugar de la BD de producción.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


# ==================== SAMPLE DATA FIXTURES ====================

@pytest.fixture
def sample_organizacion(test_db):
    """
    Crea una organización de ejemplo con un email.
    
    Returns:
        Organizacion: Instancia de organización con nombre "OrgTest"
    """
    from app.models.organizacion import Organizacion, EmailOrganizacion
    
    org = Organizacion(nombre="OrgTest", tipo="ONG")
    test_db.add(org)
    test_db.flush()
    
    email = EmailOrganizacion(nombre_organizacion="OrgTest", email="test@org.com")
    test_db.add(email)
    test_db.commit()
    
    return org


@pytest.fixture
def sample_proyecto(test_db, sample_organizacion):
    """
    Crea un proyecto de ejemplo asociado a sample_organizacion.
    
    Returns:
        Proyecto: Instancia de proyecto con fechas en 2025
    """
    from app.models.proyecto import Proyecto
    from datetime import date
    
    proyecto = Proyecto(
        nombre_organizacion=sample_organizacion.nombre,
        nombre="Proyecto Test",
        descripcion="Descripción test",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2025, 12, 31)
    )
    test_db.add(proyecto)
    test_db.commit()
    test_db.refresh(proyecto)
    
    return proyecto


@pytest.fixture
def sample_voluntario(test_db):
    """
    Crea un voluntario de ejemplo con edad válida (18+ años).
    
    Returns:
        Voluntario: Instancia con DNI "12345678A"
    """
    from app.models.voluntario import Voluntario
    from datetime import date
    
    voluntario = Voluntario(
        dni="12345678A",
        nombre="Test Voluntario",
        fecha_nacimiento=date(1990, 1, 1),
        fecha_alta=date(2020, 1, 1),
        email="voluntario@test.com"
    )
    test_db.add(voluntario)
    test_db.commit()
    
    return voluntario


@pytest.fixture
def sample_recurso_donado(test_db):
    """
    Crea un recurso donado de ejemplo.
    
    Returns:
        Recurso: Instancia de recurso donado en estado "nuevo"
    """
    from app.models.recurso import Recurso, RecursoDonado
    from datetime import date
    
    recurso = Recurso(
        nombre="Recurso Donado Test",
        fecha_entrega=date(2025, 1, 15)
    )
    test_db.add(recurso)
    test_db.flush()
    
    donado = RecursoDonado(
        id_recurso=recurso.id_recurso,
        estado="nuevo",
        nombre_donante="Donante Test"
    )
    test_db.add(donado)
    test_db.commit()
    test_db.refresh(recurso)
    
    return recurso


@pytest.fixture
def sample_recurso_alquilado(test_db):
    """
    Crea un recurso alquilado de ejemplo.
    
    Returns:
        Recurso: Instancia de recurso alquilado con proveedor
    """
    from app.models.recurso import Recurso, RecursoAlquilado
    from datetime import date
    from decimal import Decimal
    
    recurso = Recurso(
        nombre="Recurso Alquilado Test",
        fecha_entrega=date(2025, 1, 15)
    )
    test_db.add(recurso)
    test_db.flush()
    
    alquilado = RecursoAlquilado(
        id_recurso=recurso.id_recurso,
        proveedor="Proveedor Test",
        costo=Decimal("1000.00")
    )
    test_db.add(alquilado)
    test_db.commit()
    test_db.refresh(recurso)
    
    return recurso

