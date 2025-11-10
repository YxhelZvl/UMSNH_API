# src/app/features/ciclo/infrastructure/models/ciclo_model.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class CicloDB(SQLModel, table=True):
    __tablename__ = "Ciclos"

    id_ciclo: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Identificador único del ciclo"
    )
    ciclo: str = Field(
        max_length=16,
        description="Nombre del ciclo escolar"
    )
    fecha_inicio: date = Field(description="Fecha de inicio del ciclo")
    fecha_final: date = Field(description="Fecha de finalización del ciclo")