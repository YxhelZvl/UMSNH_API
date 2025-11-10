# src/app/features/ejemplares/application/dtos.py
from pydantic import BaseModel
from typing import Optional

class CreateEjemplarDTO(BaseModel):
    id_catalogo: int
    codigo_inventario: str
    ubicacion: str
    id_laboratorio: Optional[int] = None
    id_biblioteca: Optional[int] = None
    estado: str = "disponible"

class UpdateEjemplarDTO(BaseModel):
    id_catalogo: Optional[int] = None
    codigo_inventario: Optional[str] = None
    ubicacion: Optional[str] = None
    id_laboratorio: Optional[int] = None
    id_biblioteca: Optional[int] = None
    estado: Optional[str] = None