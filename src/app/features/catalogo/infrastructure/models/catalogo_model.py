# src/app/features/catalogo/infrastructure/models/catalogo_model.py
from sqlmodel import SQLModel, Field
from typing import Optional

class CatalogoDB(SQLModel, table=True):
    __tablename__ = "Catalogo"

    id_catalogo: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Identificador único del item en el catálogo"
    )
    tipo: str = Field(
        description="Tipo de item: herramienta, libro, equipo"
    )
    nombre: str = Field(
        max_length=200,
        description="Nombre del item"
    )
    autor: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Autor del libro (solo para libros)"
    )
    isbn: Optional[str] = Field(
        default=None,
        max_length=30,
        description="ISBN del libro (solo para libros)"
    )
    descripcion: Optional[str] = Field(
        default=None,
        description="Descripción del item"
    )