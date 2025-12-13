"""
Schemas del dominio de Voluntario
"""
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class VoluntarioBase(BaseModel):
    """Schema base para Voluntario"""
    nombre: str = Field(..., max_length=100, description="Nombre completo del voluntario")
    fecha_nacimiento: date = Field(..., description="Fecha de nacimiento")
    email: EmailStr = Field(..., description="Email del voluntario")


class VoluntarioCreate(VoluntarioBase):
    """
    Schema para crear un voluntario
    Valida que tenga al menos 18 años en la fecha de alta
    """
    dni: str = Field(..., max_length=9, description="DNI del voluntario (formato: 12345678A)")
    fecha_alta: date = Field(..., description="Fecha de alta en el sistema")

    @field_validator('fecha_alta')
    @classmethod
    def validar_edad_minima(cls, v, info):
        if 'fecha_nacimiento' in info.data:
            fecha_nacimiento = info.data['fecha_nacimiento']
            # Calcular edad en años
            edad_dias = (v - fecha_nacimiento).days
            edad_años = edad_dias / 365.25
            
            if edad_años < 18:
                raise ValueError(f'El voluntario debe tener al menos 18 años. Edad calculada: {edad_años:.1f} años')
            
            if v <= fecha_nacimiento:
                raise ValueError('fecha_alta debe ser posterior a fecha_nacimiento')
        
        return v


class VoluntarioUpdate(BaseModel):
    """Schema para actualizar un voluntario"""
    nombre: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None

    model_config = ConfigDict(from_attributes=True)


class VoluntarioResponse(VoluntarioBase):
    """Schema de respuesta para Voluntario"""
    dni: str
    fecha_alta: date

    model_config = ConfigDict(from_attributes=True)


class VoluntarioConEdad(VoluntarioResponse):
    """Schema de respuesta con edad calculada (desde vista)"""
    edad: int = Field(..., description="Edad calculada automáticamente")

    model_config = ConfigDict(from_attributes=True)


class SkillBase(BaseModel):
    """Schema base para Skill de voluntario"""
    nombre_skill: str = Field(..., max_length=100, description="Nombre de la habilidad")
    descripcion: Optional[str] = Field(None, description="Descripción de la habilidad")


class SkillCreate(SkillBase):
    """Schema para crear un skill"""
    pass


class SkillResponse(SkillBase):
    """Schema de respuesta para Skill"""
    dni_voluntario: str

    model_config = ConfigDict(from_attributes=True)
