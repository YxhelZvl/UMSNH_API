# src/app/features/administrativo/application/dtos.py
from pydantic import BaseModel
from typing import Optional

class CreateAdministrativoDTO(BaseModel):
    id_usuario: int
    departamento: str

class UpdateAdministrativoDTO(BaseModel):
    departamento: Optional[str] = None