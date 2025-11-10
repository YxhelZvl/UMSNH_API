# src/app/features/rol/infrastructure/models/rol_model.py
from sqlmodel import SQLModel, Field
from typing import Optional

class RolDB(SQLModel, table=True):
    __tablename__ = "Roles"

    id_rol: Optional[int] = Field(
        default=None, 
        primary_key=True, 
        description="Identificador único del rol"
    )
    tipo_rol: str = Field(
        max_length=30, 
        unique=True, 
        index=True,
        description="Tipo de rol: Estudiante, Maestro, etc."
    )