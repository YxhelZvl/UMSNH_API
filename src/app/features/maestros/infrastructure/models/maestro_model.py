# src/app/features/maestros/infrastructure/models/maestro_model.py
from sqlmodel import SQLModel, Field
from typing import Optional

class MaestroDB(SQLModel, table=True):
    __tablename__ = "Maestros"

    id_maestro: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Identificador único del maestro"
    )
    id_usuario: int = Field(
        foreign_key="Usuarios.id_usuario",
        unique=True,
        description="ID del usuario asociado al maestro"
    )