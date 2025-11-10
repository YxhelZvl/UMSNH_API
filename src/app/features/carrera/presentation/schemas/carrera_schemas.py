# src/app/features/carrera/presentation/schemas/carrera_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from src.app.shared.schemas.generic_response import GenericResponse

class CarreraCreateRequest(BaseModel):
    carrera: str = Field(..., min_length=5, max_length=120, description="Nombre de la carrera")
    facultad: str = Field(..., min_length=3, max_length=250, description="Facultad de la carrera")

class CarreraUpdateRequest(BaseModel):
    carrera: Optional[str] = Field(None, min_length=5, max_length=120, description="Nombre de la carrera")
    facultad: Optional[str] = Field(None, min_length=3, max_length=250, description="Facultad de la carrera")

class CarreraResponse(BaseModel):
    id_carrera: int
    carrera: str
    facultad: str

    class Config:
        from_attributes = True

CarrerasListResponse = GenericResponse[List[CarreraResponse]]
CarreraSingleResponse = GenericResponse[CarreraResponse]
CarreraDeleteResponse = GenericResponse[None]