"""
Modelos del dominio de Proyecto, Actividad y Localización
"""
from sqlalchemy import Column, String, Integer, Text, Date, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, CheckConstraint, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base


class Proyecto(Base):
    """
    Modelo para proyectos humanitarios
    Nota: id_proyecto es VARCHAR (alfanumérico), ej: 'P1_1'
    """
    __tablename__ = "proyecto"

    id_proyecto = Column(Integer, primary_key=True)
    nombre_organizacion = Column(String(100), ForeignKey("organizacion.nombre", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint('fecha_inicio <= fecha_fin', name='check_proyecto_fechas'),
    )

    # Relaciones
    organizacion = relationship("Organizacion", back_populates="proyectos")
    actividades = relationship("Actividad", back_populates="proyecto", cascade="all, delete-orphan")
    recursos_usados = relationship("RecursoUsado", back_populates="proyecto", cascade="all, delete-orphan")
    cesiones = relationship("Cesion", back_populates="proyecto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Proyecto(id='{self.id_proyecto}', nombre='{self.nombre}')>"


class Actividad(Base):
    """
    Modelo para actividades dentro de proyectos (entidad débil)
    Clave primaria compuesta: (id_actividad, id_proyecto)
    """
    __tablename__ = "actividad"

    id_actividad = Column(Integer, nullable=False, autoincrement=True)
    id_proyecto = Column(Integer, ForeignKey("proyecto.id_proyecto", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)

    # Clave primaria compuesta y constraints
    __table_args__ = (
        PrimaryKeyConstraint('id_actividad', 'id_proyecto'),
        CheckConstraint('fecha_inicio <= fecha_fin', name='check_actividad_fechas'),
    )

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="actividades")
    localizaciones = relationship("Localizacion", back_populates="actividad", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Actividad(id='{self.id_actividad}', proyecto='{self.id_proyecto}')>"


class Localizacion(Base):
    """
    Modelo para localizaciones geográficas de actividades (entidad débil)
    Clave primaria compuesta: (id_localizacion, id_actividad, id_proyecto)
    """
    __tablename__ = "localizacion"

    id_localizacion = Column(Integer, nullable=False, autoincrement=True)
    id_actividad = Column(Integer, nullable=False)
    id_proyecto = Column(Integer, nullable=False)
    latitud = Column(DECIMAL(10, 8), nullable=False)
    longitud = Column(DECIMAL(11, 8), nullable=False)
    descripcion = Column(String(200), nullable=False)
    observaciones = Column(Text)

    # Clave primaria compuesta y constraints
    __table_args__ = (
        PrimaryKeyConstraint('id_localizacion', 'id_actividad', 'id_proyecto'),
        ForeignKeyConstraint(
            ['id_actividad', 'id_proyecto'], 
            ['actividad.id_actividad', 'actividad.id_proyecto'], 
            ondelete='CASCADE'
        ),
        CheckConstraint('latitud >= -90 AND latitud <= 90', name='check_latitud'),
        CheckConstraint('longitud >= -180 AND longitud <= 180', name='check_longitud'),
    )

    # Relaciones
    actividad = relationship("Actividad", back_populates="localizaciones", foreign_keys=[id_actividad, id_proyecto])
    participaciones = relationship("Participa", back_populates="localizacion", cascade="all, delete-orphan")
    coordinaciones = relationship("Coordina", back_populates="localizacion", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Localizacion(id='{self.id_localizacion}', lat={self.latitud}, lon={self.longitud})>"
