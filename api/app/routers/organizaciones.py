"""
Router para endpoints de Organización
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas.organizacion import (
    OrganizacionCreate,
    OrganizacionUpdate,
    OrganizacionResponse,
    EmailOrganizacionCreate,
    EmailOrganizacionResponse
)
from app.schemas.common import PaginatedResponse, DeleteResponse, CascadeInfo
from app.crud import organizacion as crud
from app.crud.cascade import count_cascade_deletes

router = APIRouter()


@router.post("/organizaciones", response_model=OrganizacionResponse, status_code=status.HTTP_201_CREATED)
def create_organizacion(org: OrganizacionCreate, db: Session = Depends(get_db)):
    """Crea una nueva organización con sus emails"""
    # Verificar que no existe
    db_org = crud.get_organizacion(db, nombre=org.nombre)
    if db_org:
        raise HTTPException(status_code=400, detail="La organización ya existe")
    
    db_org = crud.create_organizacion(db=db, org=org)
    
    # Serializar emails a lista de strings
    return OrganizacionResponse(
        nombre=db_org.nombre,
        tipo=db_org.tipo,
        emails=[email.email for email in db_org.emails]
    )


@router.get("/organizaciones", response_model=PaginatedResponse[OrganizacionResponse])
def list_organizaciones(
    skip: int = Query(0, ge=0, description="N?mero de registros a saltar"),
    limit: int = Query(20, ge=1, le=100, description="N?mero m?ximo de registros"),
    db: Session = Depends(get_db)
):
    """Lista todas las organizaciones con paginaci?n"""
    items, total = crud.get_organizaciones(db, skip=skip, limit=limit)
    
    # Serializar emails a lista de strings
    serialized_items = [
        OrganizacionResponse(
            nombre=org.nombre,
            tipo=org.tipo,
            emails=[email.email for email in org.emails]
        )
        for org in items
    ]
    
    return PaginatedResponse(items=serialized_items, total=total, skip=skip, limit=limit)


@router.get("/organizaciones/{nombre}", response_model=OrganizacionResponse)
def get_organizacion(nombre: str, db: Session = Depends(get_db)):
    """Obtiene una organización por nombre"""
    db_org = crud.get_organizacion(db, nombre=nombre)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    
    return OrganizacionResponse(
        nombre=db_org.nombre,
        tipo=db_org.tipo,
        emails=[email.email for email in db_org.emails]
    )


@router.put("/organizaciones/{nombre}", response_model=OrganizacionResponse)
def update_organizacion(
    nombre: str,
    org: OrganizacionUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza una organización"""
    db_org = crud.update_organizacion(db, nombre=nombre, org=org)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    
    return OrganizacionResponse(
        nombre=db_org.nombre,
        tipo=db_org.tipo,
        emails=[email.email for email in db_org.emails]
    )


@router.delete("/organizaciones/{nombre}", response_model=DeleteResponse)
def delete_organizacion(nombre: str, db: Session = Depends(get_db)):
    """
    Elimina una organización y todos sus registros relacionados en cascada.
    ADVERTENCIA: Esto eliminará proyectos, actividades, localizaciones y más.
    """
    # Verificar que existe
    db_org = crud.get_organizacion(db, nombre=nombre)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    
    # Contar registros que serán eliminados
    cascade_info = count_cascade_deletes(db, "organizacion", nombre)
    
    # Eliminar
    success = crud.delete_organizacion(db, nombre=nombre)
    if not success:
        raise HTTPException(status_code=500, detail="Error al eliminar la organización")
    
    return DeleteResponse(
        message="Organización eliminada exitosamente",
        deleted_id=nombre,
        cascade_info=CascadeInfo(**cascade_info)
    )


# Endpoints para emails de organización

@router.get("/organizaciones/{nombre}/emails", response_model=List[str])
def get_emails_organizacion(nombre: str, db: Session = Depends(get_db)):
    """Lista los emails de una organización"""
    db_org = crud.get_organizacion(db, nombre=nombre)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    
    return [email.email for email in db_org.emails]


@router.post(
    "/organizaciones/{nombre}/emails",
    response_model=EmailOrganizacionResponse,
    status_code=status.HTTP_201_CREATED
)
def add_email_organizacion(
    nombre: str,
    email_data: EmailOrganizacionCreate,
    db: Session = Depends(get_db)
):
    """Agrega un email a una organización"""
    # Verificar que la organización existe
    db_org = crud.get_organizacion(db, nombre=nombre)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    
    try:
        db_email = crud.add_email_organizacion(db, nombre, email_data.email)
        return db_email
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al agregar email: {str(e)}")


@router.delete("/organizaciones/{nombre}/emails/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_email_organizacion(nombre: str, email: str, db: Session = Depends(get_db)):
    """Elimina un email de una organización"""
    success = crud.delete_email_organizacion(db, nombre, email)
    if not success:
        raise HTTPException(status_code=404, detail="Email no encontrado")
    
    return None
