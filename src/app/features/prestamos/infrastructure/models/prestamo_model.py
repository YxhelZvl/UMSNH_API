# src/app/features/prestamos/infrastructure/models/prestamo_model.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date

class PrestamoDB(SQLModel, table=True):
    __tablename__ = "Prestamos"

    id_prestamo: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Identificador único del préstamo"
    )
    id_usuario: int = Field(
        foreign_key="Usuarios.id_usuario",
        description="ID del usuario que realiza el préstamo"
    )
    id_ejemplar: int = Field(
        foreign_key="Ejemplares.id_ejemplar",
        description="ID del ejemplar prestado"
    )
    fecha_prestamo: datetime = Field(
        default_factory=datetime.now,
        description="Fecha y hora en que se realizó el préstamo"
    )
    fecha_devolucion_esperada: date = Field(
        description="Fecha esperada para la devolución del ejemplar"
    )
    fecha_devolucion_real: Optional[datetime] = Field(
        default=None,
        description="Fecha y hora real en que se devolvió el ejemplar"
    )
    estado: str = Field(
        default="activo",
        description="Estado del préstamo: activo, completado, retrasado"
    )