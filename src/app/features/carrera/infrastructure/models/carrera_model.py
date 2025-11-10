# src/app/features/carrera/infrastructure/models/carrera_model.py
from sqlmodel import SQLModel, Field
from typing import Optional

class CarreraDB(SQLModel, table=True):
    __tablename__ = "Carreras"

    id_carrera: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Identificador único de la carrera"
    )
    carrera: str = Field(
        max_length=120,
        description="Nombre de la carrera"
    )
    facultad: str = Field(
        max_length=250,
        description="Facultad a la que pertenece la carrera"
    )