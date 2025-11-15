# src/app/features/ciclo/presentation/schemas/ciclo_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from src.app.shared.schemas.generic_response import GenericResponse

class CicloCreateRequest(BaseModel):
    ciclo: str = Field(..., max_length=16, description="Nombre del ciclo (formato: YYYY-YYYY)")
    fecha_inicio: date = Field(..., description="Fecha de inicio del ciclo")
    fecha_final: date = Field(..., description="Fecha de finalización del ciclo")

class CicloUpdateRequest(BaseModel):
    ciclo: Optional[str] = Field(None, max_length=16, description="Nombre del ciclo (formato: YYYY-YYYY)")
    fecha_inicio: Optional[date] = Field(None, description="Fecha de inicio del ciclo")
    fecha_final: Optional[date] = Field(None, description="Fecha de finalización del ciclo")

class CicloResponse(BaseModel):
    id_ciclo: int
    ciclo: str
    fecha_inicio: date
    fecha_final: date
    
class LastIdCycleResponse(BaseModel):
    last_id_cycle: Optional[int]
    

    class Config:
        from_attributes = True

CiclosListResponse = GenericResponse[List[CicloResponse]]
CicloSingleResponse = GenericResponse[CicloResponse]
CicloDeleteResponse = GenericResponse[None]
LastSingleIdCycleResponse = GenericResponse[LastIdCycleResponse]