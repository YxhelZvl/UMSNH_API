# src/app/features/maestros/domain/entities/maestro.py
from pydantic import BaseModel
from typing import Optional

class Maestro(BaseModel):
    id_maestro: Optional[int] = None
    id_usuario: int

    class Config:
        arbitrary_types_allowed = True