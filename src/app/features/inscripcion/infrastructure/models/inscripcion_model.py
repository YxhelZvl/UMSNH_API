# src/app/features/inscripcion/infrastructure/models/inscripcion_model.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class InscripcionDB(SQLModel, table=True):
    __tablename__ = "Inscripciones"

    id_inscripcion: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Identificador único de la inscripción"
    )
    id_usuario: int = Field(
        foreign_key="Usuarios.id_usuario",
        description="ID del usuario"
    )
    id_ciclo: int = Field(
        foreign_key="Ciclos.id_ciclo",
        description="ID del ciclo"
    )
    fecha_inscripcion: date = Field(
        description="Fecha de inscripción"
    )
    estado: str = Field(
        description="Estado de la inscripción: activa, en_proceso, finalizada"
    )