"""
Schemas del dominio de Proyecto, Actividad y Localización
"""
from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ProyectoBase(BaseModel):
    """
    Schema base para Proyecto
    Nota: id_proyecto es VARCHAR (alfanumérico), ej: 'P1_1'
    """
    nombre: str = Field(..., max_length=100, description="Nombre del proyecto")
    descripcion: Optional[str] = Field(None, description="Descripción detallada del proyecto")
    fecha_inicio: date = Field(..., description="Fecha de inicio del proyecto")
    fecha_fin: date = Field(..., description="Fecha de finalización del proyecto")

    @field_validator('fecha_fin')
    @classmethod
    def validar_fechas(cls, v, info):
        if 'fecha_inicio' in info.data and v < info.data['fecha_inicio']:
            raise ValueError('fecha_fin debe ser mayor o igual a fecha_inicio')
        return v


class ProyectoCreate(ProyectoBase):
    """Schema para crear un proyecto"""
    nombre_organizacion: str = Field(..., max_length=100, description="Nombre de la organización")


class ProyectoUpdate(BaseModel):
    """Schema para actualizar un proyecto"""
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class ProyectoResponse(ProyectoBase):
    """Schema de respuesta para Proyecto"""
    id_proyecto: int
    nombre_organizacion: str

    model_config = ConfigDict(from_attributes=True)


class ActividadBase(BaseModel):
    """
    Schema base para Actividad
    Nota: id_actividad es VARCHAR (alfanumérico), ej: 'A1_1_1'
    """
    nombre: str = Field(..., max_length=100, description="Nombre de la actividad")
    descripcion: Optional[str] = Field(None, description="Descripción de la actividad")
    fecha_inicio: date = Field(..., description="Fecha de inicio")
    fecha_fin: date = Field(..., description="Fecha de finalización")

    @field_validator('fecha_fin')
    @classmethod
    def validar_fechas(cls, v, info):
        if 'fecha_inicio' in info.data and v < info.data['fecha_inicio']:
            raise ValueError('fecha_fin debe ser mayor o igual a fecha_inicio')
        return v


class ActividadCreate(ActividadBase):
    """Schema para crear una actividad"""
    pass  # id_actividad se asigna automáticamente


class ActividadUpdate(BaseModel):
    """Schema para actualizar una actividad"""
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class ActividadResponse(ActividadBase):
    """Schema de respuesta para Actividad"""
    id_actividad: int
    id_proyecto: int

    model_config = ConfigDict(from_attributes=True)


class LocalizacionBase(BaseModel):
    """
    Schema base para Localización
    Nota: id_localizacion es VARCHAR (alfanumérico), ej: 'L1_1_1_1'
    """
    latitud: Decimal = Field(
        ...,
        ge=-90,
        le=90,
        decimal_places=8,
        description="Latitud (rango: -90 a 90)"
    )
    longitud: Decimal = Field(
        ...,
        ge=-180,
        le=180,
        decimal_places=8,
        description="Longitud (rango: -180 a 180)"
    )
    descripcion: str = Field(..., max_length=200, description="Descripción de la localización")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")


class LocalizacionCreate(LocalizacionBase):
    """Schema para crear una localización"""
    pass  # id_localizacion se asigna automáticamente


class LocalizacionUpdate(BaseModel):
    """Schema para actualizar una localización"""
    latitud: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitud: Optional[Decimal] = Field(None, ge=-180, le=180)
    descripcion: Optional[str] = Field(None, max_length=200)
    observaciones: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class LocalizacionResponse(LocalizacionBase):
    """Schema de respuesta para Localización"""
    id_localizacion: int
    id_actividad: int
    id_proyecto: int

    model_config = ConfigDict(from_attributes=True)
