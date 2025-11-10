# src/app/features/bibliotecas/infrastructure/models/biblioteca_model.py
from sqlmodel import SQLModel, Field
from typing import Optional

class BibliotecaDB(SQLModel, table=True):
    __tablename__ = "Bibliotecas"

    id_biblioteca: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Identificador único de la biblioteca"
    )
    nombre: str = Field(
        max_length=150,
        unique=True,
        description="Nombre de la biblioteca"
    )
    ubicacion: str = Field(
        max_length=250,
        description="Ubicación de la biblioteca"
    )