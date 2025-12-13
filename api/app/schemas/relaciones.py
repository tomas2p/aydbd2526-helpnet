"""
Schemas de relaciones N:M y ternarias
"""
from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class ParticipaBase(BaseModel):
    """Schema base para Participa (voluntario con rol operativo)"""
    rol: str = Field(..., max_length=50, description="Rol del voluntario en la localización")
    evaluacion: Optional[int] = Field(None, ge=0, le=10, description="Evaluación del desempeño (0-10)")


class ParticipaCreate(ParticipaBase):
    """Schema para crear una participación"""
    id_localizacion: int = Field(..., description="ID de la localización")
    id_actividad: int = Field(..., description="ID de la actividad")
    id_proyecto: int = Field(..., description="ID del proyecto")
    dni_voluntario: str = Field(..., description="DNI del voluntario")


class ParticipaUpdate(BaseModel):
    """Schema para actualizar una participación"""
    rol: Optional[str] = Field(None, max_length=50)
    evaluacion: Optional[int] = Field(None, ge=0, le=10)

    model_config = ConfigDict(from_attributes=True)


class ParticipaResponse(ParticipaBase):
    """Schema de respuesta para Participa"""
    id_localizacion: int
    id_actividad: int
    id_proyecto: int
    dni_voluntario: str

    model_config = ConfigDict(from_attributes=True)


class CoordinaBase(BaseModel):
    """Schema base para Coordina (voluntario responsable)"""
    evaluacion: Optional[int] = Field(None, ge=0, le=10, description="Evaluación del desempeño (0-10)")


class CoordinaCreate(CoordinaBase):
    """Schema para crear una coordinación"""
    id_localizacion: int = Field(..., description="ID de la localización")
    id_actividad: int = Field(..., description="ID de la actividad")
    id_proyecto: int = Field(..., description="ID del proyecto")
    dni_voluntario: str = Field(..., description="DNI del voluntario coordinador")


class CoordinaUpdate(BaseModel):
    """Schema para actualizar una coordinación"""
    evaluacion: Optional[int] = Field(None, ge=0, le=10)

    model_config = ConfigDict(from_attributes=True)


class CoordinaResponse(CoordinaBase):
    """Schema de respuesta para Coordina"""
    id_localizacion: int
    id_actividad: int
    id_proyecto: int
    dni_voluntario: str

    model_config = ConfigDict(from_attributes=True)


class CesionBase(BaseModel):
    """Schema base para Cesión (relación ternaria)"""
    fecha_cesion: date = Field(..., description="Fecha de la cesión")
    duracion: int = Field(..., gt=0, description="Duración en días (debe ser positiva)")


class CesionCreate(CesionBase):
    """Schema para crear una cesión"""
    nombre_organizacion: str = Field(..., max_length=100, description="Nombre de la organización")
    id_proyecto: int = Field(..., description="ID del proyecto")
    dni_voluntario: str = Field(..., description="DNI del voluntario")


class CesionUpdate(BaseModel):
    """Schema para actualizar una cesión"""
    fecha_cesion: Optional[date] = None
    duracion: Optional[int] = Field(None, gt=0)

    model_config = ConfigDict(from_attributes=True)


class CesionResponse(CesionBase):
    """Schema de respuesta para Cesión"""
    nombre_organizacion: str
    id_proyecto: int
    dni_voluntario: str

    model_config = ConfigDict(from_attributes=True)


class RecursoUsadoCreate(BaseModel):
    """Schema para asignar recurso a proyecto"""
    id_proyecto: int = Field(..., description="ID del proyecto")
    id_recurso: int = Field(..., description="ID del recurso")


class RecursoUsadoResponse(RecursoUsadoCreate):
    """Schema de respuesta para RecursoUsado"""
    
    model_config = ConfigDict(from_attributes=True)
