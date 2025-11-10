# src/app/features/laboratorios/application/dtos.py
from pydantic import BaseModel
from typing import Optional

class CreateLaboratorioDTO(BaseModel):
    nombre: str
    ubicacion: str
    responsable_id: Optional[int] = None

class UpdateLaboratorioDTO(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    responsable_id: Optional[int] = None