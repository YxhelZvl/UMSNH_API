# src/app/features/administrativo/domain/entities/administrativo.py
from pydantic import BaseModel
from typing import Optional

class Administrativo(BaseModel):
    id_administrativo: Optional[int] = None
    id_usuario: int
    departamento: str

    class Config:
        arbitrary_types_allowed = True