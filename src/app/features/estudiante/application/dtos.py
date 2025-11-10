# src/app/features/estudiante/application/dtos.py
from pydantic import BaseModel
from typing import Optional

class CreateEstudianteDTO(BaseModel):
    id_usuario: int
    id_carrera: int

class UpdateEstudianteDTO(BaseModel):
    id_carrera: Optional[int] = None