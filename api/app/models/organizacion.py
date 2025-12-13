"""
Modelos del dominio de Organización
"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Organizacion(Base):
    """
    Modelo para organizaciones (ONGs, fundaciones, etc.)
    """
    __tablename__ = "organizacion"

    nombre = Column(String(100), primary_key=True)
    tipo = Column(String(50), nullable=False)

    # Relaciones
    emails = relationship("EmailOrganizacion", back_populates="organizacion", cascade="all, delete-orphan")
    proyectos = relationship("Proyecto", back_populates="organizacion", cascade="all, delete-orphan")
    cesiones = relationship("Cesion", back_populates="organizacion", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Organizacion(nombre='{self.nombre}', tipo='{self.tipo}')>"


class EmailOrganizacion(Base):
    """
    Modelo para emails de organizaciones (atributo multivalor)
    """
    __tablename__ = "email_organizacion"

    nombre_organizacion = Column(String(100), ForeignKey("organizacion.nombre", ondelete="CASCADE"), primary_key=True)
    email = Column(String(100), primary_key=True)

    # Relaciones
    organizacion = relationship("Organizacion", back_populates="emails")

    def __repr__(self):
        return f"<EmailOrganizacion(org='{self.nombre_organizacion}', email='{self.email}')>"
