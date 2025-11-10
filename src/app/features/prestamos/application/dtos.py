# src/app/features/prestamos/application/dtos.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class CreatePrestamoDTO(BaseModel):
    id_usuario: int
    id_ejemplar: int
    fecha_devolucion_esperada: date
    estado: str = "activo"

class UpdatePrestamoDTO(BaseModel):
    id_usuario: Optional[int] = None
    id_ejemplar: Optional[int] = None
    fecha_devolucion_esperada: Optional[date] = None
    estado: Optional[str] = None

class DevolverPrestamoDTO(BaseModel):
    fecha_devolucion_real: Optional[date] = None

class RenovarPrestamoDTO(BaseModel):
    nueva_fecha_devolucion: date