"""
Modelos del dominio de Voluntario
"""
from sqlalchemy import Column, String, Date, ForeignKey, CheckConstraint, Integer, select, func
from sqlalchemy.orm import relationship
from app.database import Base


class Voluntario(Base):
    """
    Modelo para voluntarios
    """
    __tablename__ = "voluntario"

    dni = Column(String(9), primary_key=True)
    nombre = Column(String(100), nullable=False)
    fecha_alta = Column(Date, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    email = Column(String(100), nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint('fecha_nacimiento < fecha_alta', name='check_fechas_voluntario'),
        CheckConstraint("fecha_alta >= fecha_nacimiento + INTERVAL '18 years'", name='check_edad_minima'),
    )

    # Relaciones
    skills = relationship("VoluntarioSkill", back_populates="voluntario", cascade="all, delete-orphan")
    participaciones = relationship("Participa", back_populates="voluntario", cascade="all, delete-orphan")
    coordinaciones = relationship("Coordina", back_populates="voluntario", cascade="all, delete-orphan")
    cesiones = relationship("Cesion", back_populates="voluntario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Voluntario(dni='{self.dni}', nombre='{self.nombre}')>"


class VoluntarioSkill(Base):
    """
    Modelo para habilidades de voluntarios (atributo multivalor)
    """
    __tablename__ = "voluntario_skill"

    dni_voluntario = Column(String(9), ForeignKey("voluntario.dni", ondelete="CASCADE"), primary_key=True)
    nombre_skill = Column(String(100), primary_key=True)
    descripcion = Column(String)

    # Relaciones
    voluntario = relationship("Voluntario", back_populates="skills")

    def __repr__(self):
        return f"<VoluntarioSkill(dni='{self.dni_voluntario}', skill='{self.nombre_skill}')>"


class VistaVoluntarioEdad(Base):
    """
    Vista para voluntarios con edad calculada automáticamente
    NOTA: Esta es una vista READ-ONLY, no permite INSERT/UPDATE/DELETE
    """
    __tablename__ = "vista_voluntario_edad"
    __table_args__ = {'info': {'is_view': True}}

    dni = Column(String(9), primary_key=True)
    nombre = Column(String(100))
    fecha_alta = Column(Date)
    fecha_nacimiento = Column(Date)
    email = Column(String(100))
    edad = Column(Integer)  # Calculado por la vista

    def __repr__(self):
        return f"<VistaVoluntarioEdad(dni='{self.dni}', nombre='{self.nombre}', edad={self.edad})>"
