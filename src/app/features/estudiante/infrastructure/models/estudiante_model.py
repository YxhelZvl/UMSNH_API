# src/app/features/estudiante/infrastructure/models/estudiante_model.py
from sqlmodel import SQLModel, Field
from typing import Optional

class EstudianteDB(SQLModel, table=True):
    __tablename__ = "Estudiantes"

    id_estudiante: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Identificador único del estudiante"
    )
    id_usuario: int = Field(
        foreign_key="Usuarios.id_usuario",
        unique=True,
        description="ID del usuario asociado al estudiante"
    )
    id_carrera: int = Field(
        foreign_key="Carreras.id_carrera",
        description="ID de la carrera del estudiante"
    )