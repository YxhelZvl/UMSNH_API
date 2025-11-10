# src/app/features/maestros/application/dtos.py
from pydantic import BaseModel

class CreateMaestroDTO(BaseModel):
    id_usuario: int

class UpdateMaestroDTO(BaseModel):
    # No hay campos para actualizar en esta versión simple
    pass