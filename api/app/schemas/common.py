"""
Schemas comunes y genéricos
"""
from typing import TypeVar, Generic, List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Respuesta paginada genérica para listados
    """
    items: List[T]
    total: int
    skip: int
    limit: int

    model_config = ConfigDict(from_attributes=True)


class CascadeInfo(BaseModel):
    """
    Información sobre registros eliminados en cascada
    """
    proyectos: int = 0
    actividades: int = 0
    localizaciones: int = 0
    participaciones: int = 0
    coordinaciones: int = 0
    cesiones: int = 0
    recursos_usados: int = 0
    emails: int = 0
    skills: int = 0

    model_config = ConfigDict(from_attributes=True)


class DeleteResponse(BaseModel):
    """
    Respuesta para operaciones DELETE exitosas
    """
    message: str
    deleted_id: Any
    cascade_info: Optional[CascadeInfo] = None

    model_config = ConfigDict(from_attributes=True)
