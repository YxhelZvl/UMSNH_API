# src/app/features/carrera/application/dtos.py
from pydantic import BaseModel
from typing import Optional

class CreateCarreraDTO(BaseModel):
    carrera: str
    facultad: str

class UpdateCarreraDTO(BaseModel):
    carrera: Optional[str] = None
    facultad: Optional[str] = None