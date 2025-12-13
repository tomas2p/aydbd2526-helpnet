"""
Schemas del dominio de Organización
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class OrganizacionBase(BaseModel):
    """Schema base para Organización"""
    nombre: str = Field(..., max_length=100, description="Nombre único de la organización")
    tipo: str = Field(..., max_length=50, description="Tipo de organización (ONG, Fundación, etc.)")


class OrganizacionCreate(OrganizacionBase):
    """Schema para crear una organización"""
    emails: List[str] = Field(default_factory=list, description="Lista de emails de la organización")


class OrganizacionUpdate(BaseModel):
    """Schema para actualizar una organización"""
    tipo: Optional[str] = Field(None, max_length=50)

    model_config = ConfigDict(from_attributes=True)


class OrganizacionResponse(OrganizacionBase):
    """Schema de respuesta para Organización"""
    emails: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class EmailOrganizacionCreate(BaseModel):
    """Schema para agregar email a organización"""
    email: EmailStr = Field(..., description="Email a agregar")


class EmailOrganizacionResponse(BaseModel):
    """Schema de respuesta para email de organización"""
    nombre_organizacion: str
    email: str

    model_config = ConfigDict(from_attributes=True)
