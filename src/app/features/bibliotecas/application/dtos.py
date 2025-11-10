# src/app/features/bibliotecas/application/dtos.py
from pydantic import BaseModel
from typing import Optional

class CreateBibliotecaDTO(BaseModel):
    nombre: str
    ubicacion: str

class UpdateBibliotecaDTO(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None