# src/app/features/catalogo/application/dtos.py
from pydantic import BaseModel
from typing import Optional

class CreateCatalogoDTO(BaseModel):
    tipo: str
    nombre: str
    autor: Optional[str] = None
    isbn: Optional[str] = None
    descripcion: Optional[str] = None

class UpdateCatalogoDTO(BaseModel):
    tipo: Optional[str] = None
    nombre: Optional[str] = None
    autor: Optional[str] = None
    isbn: Optional[str] = None
    descripcion: Optional[str] = None