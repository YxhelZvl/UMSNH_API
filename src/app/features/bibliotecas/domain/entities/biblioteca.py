# src/app/features/bibliotecas/domain/entities/biblioteca.py
from pydantic import BaseModel
from typing import Optional

class Biblioteca(BaseModel):
    id_biblioteca: Optional[int] = None
    nombre: str
    ubicacion: str

    class Config:
        arbitrary_types_allowed = True