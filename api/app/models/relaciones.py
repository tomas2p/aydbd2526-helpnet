"""
Modelos de relaciones N:M y ternarias
"""
from sqlalchemy import Column, String, Integer, Date, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Participa(Base):
    """
    Modelo para participación de voluntarios en localizaciones (rol operativo)
    Relación N:M con atributos propios
    Clave primaria compuesta con FK compuesta a Localizacion
    """
    __tablename__ = "participa"

    id_localizacion = Column(Integer, nullable=False)
    id_actividad = Column(Integer, nullable=False)
    id_proyecto = Column(Integer, nullable=False)
    dni_voluntario = Column(String(9), ForeignKey("voluntario.dni", ondelete="CASCADE"), nullable=False)
    rol = Column(String(50), nullable=False)
    evaluacion = Column(Integer)

    # Clave primaria compuesta y constraints
    __table_args__ = (
        PrimaryKeyConstraint('id_localizacion', 'id_actividad', 'id_proyecto', 'dni_voluntario'),
        ForeignKeyConstraint(
            ['id_localizacion', 'id_actividad', 'id_proyecto'],
            ['localizacion.id_localizacion', 'localizacion.id_actividad', 'localizacion.id_proyecto'],
            ondelete='CASCADE'
        ),
        CheckConstraint('evaluacion >= 0 AND evaluacion <= 10', name='check_evaluacion_participa'),
    )

    # Relaciones
    voluntario = relationship("Voluntario", back_populates="participaciones")
    localizacion = relationship(
        "Localizacion",
        back_populates="participaciones",
        foreign_keys=[id_localizacion, id_actividad, id_proyecto]
    )

    def __repr__(self):
        return f"<Participa(voluntario='{self.dni_voluntario}', loc='{self.id_localizacion}', rol='{self.rol}')>"


class Coordina(Base):
    """
    Modelo para coordinación de voluntarios en localizaciones (rol responsable)
    Relación N:M con atributos propios
    Clave primaria compuesta con FK compuesta a Localizacion
    """
    __tablename__ = "coordina"

    id_localizacion = Column(Integer, nullable=False)
    id_actividad = Column(Integer, nullable=False)
    id_proyecto = Column(Integer, nullable=False)
    dni_voluntario = Column(String(9), ForeignKey("voluntario.dni", ondelete="CASCADE"), nullable=False)
    evaluacion = Column(Integer)

    # Clave primaria compuesta y constraints
    __table_args__ = (
        PrimaryKeyConstraint('id_localizacion', 'id_actividad', 'id_proyecto', 'dni_voluntario'),
        ForeignKeyConstraint(
            ['id_localizacion', 'id_actividad', 'id_proyecto'],
            ['localizacion.id_localizacion', 'localizacion.id_actividad', 'localizacion.id_proyecto'],
            ondelete='CASCADE'
        ),
        CheckConstraint('evaluacion >= 0 AND evaluacion <= 10', name='check_evaluacion_coordina'),
    )

    # Relaciones
    voluntario = relationship("Voluntario", back_populates="coordinaciones")
    localizacion = relationship(
        "Localizacion",
        back_populates="coordinaciones",
        foreign_keys=[id_localizacion, id_actividad, id_proyecto]
    )

    def __repr__(self):
        return f"<Coordina(voluntario='{self.dni_voluntario}', loc='{self.id_localizacion}')>"


class Cesion(Base):
    """
    Modelo para cesión de voluntarios entre organizaciones y proyectos
    Relación ternaria con atributos propios
    """
    __tablename__ = "cesion"

    nombre_organizacion = Column(
        String(100),
        ForeignKey("organizacion.nombre", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    id_proyecto = Column(Integer, ForeignKey("proyecto.id_proyecto", ondelete="CASCADE"), primary_key=True)
    dni_voluntario = Column(String(9), ForeignKey("voluntario.dni", ondelete="CASCADE"), primary_key=True)
    fecha_cesion = Column(Date, nullable=False)
    duracion = Column(Integer, nullable=False)  # Duración en días

    # Constraints
    __table_args__ = (
        CheckConstraint('duracion > 0', name='check_duracion_positiva'),
    )

    # Relaciones
    organizacion = relationship("Organizacion", back_populates="cesiones")
    proyecto = relationship("Proyecto", back_populates="cesiones")
    voluntario = relationship("Voluntario", back_populates="cesiones")

    def __repr__(self):
        return f"<Cesion(org='{self.nombre_organizacion}', proyecto='{self.id_proyecto}', voluntario='{self.dni_voluntario}')>"


class RecursoUsado(Base):
    """
    Modelo para recursos usados en proyectos
    Relación N:M pura sin atributos adicionales
    """
    __tablename__ = "recurso_usado"

    id_proyecto = Column(Integer, ForeignKey("proyecto.id_proyecto", ondelete="CASCADE"), primary_key=True)
    id_recurso = Column(Integer, ForeignKey("recurso.id_recurso", ondelete="CASCADE"), primary_key=True)

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="recursos_usados")
    recurso = relationship("Recurso", back_populates="recursos_usados")

    def __repr__(self):
        return f"<RecursoUsado(proyecto='{self.id_proyecto}', recurso={self.id_recurso})>"
