# src/app/features/estudiante/domain/entities/estudiante.py
from pydantic import BaseModel
from typing import Optional

class Estudiante(BaseModel):
    id_estudiante: Optional[int] = None
    id_usuario: int
    id_carrera: int
    
    class Config:
        arbitrary_types_allowed = True