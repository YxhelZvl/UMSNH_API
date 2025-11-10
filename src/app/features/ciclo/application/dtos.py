# src/app/features/ciclo/application/dtos.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class CreateCicloDTO(BaseModel):
    ciclo: str
    fecha_inicio: date
    fecha_final: date

class UpdateCicloDTO(BaseModel):
    ciclo: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_final: Optional[date] = None