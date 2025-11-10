# src/app/features/ejemplares/infrastructure/models/ejemplar_model.py
from sqlmodel import SQLModel, Field
from typing import Optional

class EjemplarDB(SQLModel, table=True):
    __tablename__ = "Ejemplares"

    id_ejemplar: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Identificador único del ejemplar"
    )
    id_catalogo: int = Field(
        foreign_key="Catalogo.id_catalogo",
        description="ID del catálogo al que pertenece el ejemplar"
    )
    codigo_inventario: str = Field(
        max_length=50,
        unique=True,
        description="Código único de inventario del ejemplar"
    )
    ubicacion: str = Field(
        description="Ubicación del ejemplar: laboratorio o biblioteca"
    )
    id_laboratorio: Optional[int] = Field(
        default=None,
        foreign_key="Laboratorios.id_laboratorio",
        description="ID del laboratorio si la ubicación es laboratorio"
    )
    id_biblioteca: Optional[int] = Field(
        default=None,
        foreign_key="Bibliotecas.id_biblioteca",
        description="ID de la biblioteca si la ubicación es biblioteca"
    )
    estado: str = Field(
        default="disponible",
        description="Estado del ejemplar: no_disponible, disponible, prestado, mantenimiento, perdido"
    )