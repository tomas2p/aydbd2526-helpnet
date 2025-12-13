"""
Modelos del dominio de Recurso con herencia polimórfica
"""
from sqlalchemy import Column, String, Integer, Text, Date, ForeignKey, CheckConstraint, DECIMAL, CHAR
from sqlalchemy.orm import relationship
from app.database import Base


class Recurso(Base):
    """
    Modelo padre para recursos (tabla base para herencia)
    tipo: 'D' = Donado, 'A' = Alquilado (discriminador de herencia)
    """
    __tablename__ = "recurso"

    id_recurso = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    fecha_entrega = Column(Date, nullable=False)
    tipo = Column(CHAR(1), nullable=False)  # Discriminador polimórfico

    # Configuración de herencia polimórfica
    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'R',  # Identidad base (no se usa directamente)
    }

    # Constraints
    __table_args__ = (
        CheckConstraint("tipo IN ('D', 'A')", name='check_tipo_recurso'),
    )

    # Relaciones
    recursos_usados = relationship("RecursoUsado", back_populates="recurso", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Recurso(id={self.id_recurso}, nombre='{self.nombre}', tipo='{self.tipo}')>"


class Donado(Recurso):
    """
    Modelo para recursos donados (subclase de Recurso)
    Herencia: Table-per-Concrete-Class
    """
    __tablename__ = "donado"

    id_recurso = Column(Integer, ForeignKey("recurso.id_recurso", ondelete="CASCADE"), primary_key=True)
    estado = Column(String(50), nullable=False)
    nombre_donante = Column(String(100))
    email_donante = Column(String(100))

    # Configuración de herencia
    __mapper_args__ = {
        'polymorphic_identity': 'D',
    }

    def __repr__(self):
        return f"<Donado(id={self.id_recurso}, nombre='{self.nombre}', estado='{self.estado}')>"


class Alquilado(Recurso):
    """
    Modelo para recursos alquilados (subclase de Recurso)
    Herencia: Table-per-Concrete-Class
    """
    __tablename__ = "alquilado"

    id_recurso = Column(Integer, ForeignKey("recurso.id_recurso", ondelete="CASCADE"), primary_key=True)
    proveedor = Column(String(100), nullable=False)
    costo = Column(DECIMAL(10, 2), nullable=False)
    fecha_devolucion = Column(Date, nullable=False)

    # Configuración de herencia
    __mapper_args__ = {
        'polymorphic_identity': 'A',
    }

    # Constraints
    __table_args__ = (
        CheckConstraint('costo >= 0', name='check_costo_positivo'),
    )

    def __repr__(self):
        return f"<Alquilado(id={self.id_recurso}, nombre='{self.nombre}', proveedor='{self.proveedor}')>"
