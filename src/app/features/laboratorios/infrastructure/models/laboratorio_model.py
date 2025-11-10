# src/app/features/laboratorios/infrastructure/models/laboratorio_model.py
from sqlmodel import SQLModel, Field
from typing import Optional

class LaboratorioDB(SQLModel, table=True):
    __tablename__ = "Laboratorios"

    id_laboratorio: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Identificador único del laboratorio"
    )
    nombre: str = Field(
        max_length=150,
        unique=True,
        description="Nombre del laboratorio"
    )
    ubicacion: str = Field(
        max_length=250,
        description="Ubicación del laboratorio"
    )
    responsable_id: Optional[int] = Field(
        default=None,
        foreign_key="Usuarios.id_usuario",
        description="ID del usuario responsable del laboratorio"
    )