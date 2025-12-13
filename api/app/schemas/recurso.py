"""
Schemas del dominio de Recurso con herencia polimórfica
"""
from typing import Optional, Union, Literal
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class RecursoBase(BaseModel):
    """Schema base para Recurso"""
    nombre: str = Field(..., max_length=100, description="Nombre del recurso")
    descripcion: Optional[str] = Field(None, description="Descripción del recurso")
    fecha_entrega: date = Field(..., description="Fecha de entrega del recurso")


class RecursoDonandoCreate(RecursoBase):
    """
    Schema para crear un recurso donado
    tipo siempre es 'D' para donados
    """
    tipo: Literal['D'] = Field(default='D', description="Tipo de recurso: D=Donado")
    estado: str = Field(..., max_length=50, description="Estado del recurso donado")
    nombre_donante: Optional[str] = Field(None, max_length=100, description="Nombre del donante")
    email_donante: Optional[EmailStr] = Field(None, description="Email del donante")


class RecursoDonandoResponse(RecursoBase):
    """Schema de respuesta para recurso donado"""
    id_recurso: int
    tipo: Literal['D'] = 'D'
    estado: str
    nombre_donante: Optional[str] = None
    email_donante: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RecursoAlquiladoCreate(RecursoBase):
    """
    Schema para crear un recurso alquilado
    tipo siempre es 'A' para alquilados
    """
    tipo: Literal['A'] = Field(default='A', description="Tipo de recurso: A=Alquilado")
    proveedor: str = Field(..., max_length=100, description="Proveedor del recurso")
    costo: Decimal = Field(..., ge=0, decimal_places=2, description="Costo del alquiler")
    fecha_devolucion: date = Field(..., description="Fecha de devolución")


class RecursoAlquiladoResponse(RecursoBase):
    """Schema de respuesta para recurso alquilado"""
    id_recurso: int
    tipo: Literal['A'] = 'A'
    proveedor: str
    costo: Decimal
    fecha_devolucion: date

    model_config = ConfigDict(from_attributes=True)


# Tipo unión para respuestas polimórficas
RecursoResponse = Union[RecursoDonandoResponse, RecursoAlquiladoResponse]


def serialize_recurso(recurso_obj) -> RecursoResponse:
    """
    Serializa un objeto Recurso al schema correcto según su tipo
    
    Args:
        recurso_obj: Instancia de Donado o Alquilado
    
    Returns:
        RecursoDonandoResponse o RecursoAlquiladoResponse según corresponda
    """
    from app.models.recurso import Donado, Alquilado
    
    if isinstance(recurso_obj, Donado) or recurso_obj.tipo == 'D':
        return RecursoDonandoResponse(
            id_recurso=recurso_obj.id_recurso,
            nombre=recurso_obj.nombre,
            descripcion=recurso_obj.descripcion,
            fecha_entrega=recurso_obj.fecha_entrega,
            tipo='D',
            estado=recurso_obj.estado,
            nombre_donante=recurso_obj.nombre_donante,
            email_donante=recurso_obj.email_donante
        )
    elif isinstance(recurso_obj, Alquilado) or recurso_obj.tipo == 'A':
        return RecursoAlquiladoResponse(
            id_recurso=recurso_obj.id_recurso,
            nombre=recurso_obj.nombre,
            descripcion=recurso_obj.descripcion,
            fecha_entrega=recurso_obj.fecha_entrega,
            tipo='A',
            proveedor=recurso_obj.proveedor,
            costo=recurso_obj.costo,
            fecha_devolucion=recurso_obj.fecha_devolucion
        )
    else:
        raise ValueError(f"Tipo de recurso desconocido: {recurso_obj.tipo}")
