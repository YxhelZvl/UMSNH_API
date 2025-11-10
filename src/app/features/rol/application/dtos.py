# src/app/features/rol/application/dtos.py
from pydantic import BaseModel
from typing import Optional

class CreateRolDTO(BaseModel):
    """DTO para crear un nuevo rol"""
    tipo_rol: str

class UpdateRolDTO(BaseModel):
    """DTO para actualizar un rol existente"""
    tipo_rol: Optional[str] = None