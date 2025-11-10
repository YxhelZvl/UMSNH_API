# src/app/features/administrativo/infrastructure/models/administrativo_model.py
from sqlmodel import SQLModel, Field
from typing import Optional

class AdministrativoDB(SQLModel, table=True):
    __tablename__ = "Administrativos"

    id_administrativo: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Identificador único del administrativo"
    )
    id_usuario: int = Field(
        foreign_key="Usuarios.id_usuario",
        unique=True,
        description="ID del usuario asociado al administrativo"
    )
    departamento: str = Field(
        max_length=100,
        description="Departamento del administrativo"
    )