# src/app/features/user/infrastructure/models/user_model.py
from sqlmodel import SQLModel, Field
from typing import Optional

class UserDB(SQLModel, table=True):
    __tablename__ = "Usuarios"

    id_usuario: Optional[int] = Field(
        default=None, 
        primary_key=True, 
        description="Identificador único del usuario"
    )
    nombre: str = Field(
        max_length=40,
        description="Nombre del usuario"
    )
    apellidoP: str = Field(
        max_length=40,
        description="Apellido paterno"
    )
    apellidoM: str = Field(
        max_length=40,
        description="Apellido materno"
    )
    matricula: str = Field(
        max_length=15,
        unique=True,
        index=True,
        description="Matrícula única del usuario"
    )
    email: str = Field(
        max_length=200,
        unique=True,
        index=True,
        description="Email único del usuario"
    )
    contraseña: str = Field(
        max_length=60,
        description="Contraseña encriptada del usuario"
    )
    id_rol: int = Field(
        foreign_key="Roles.id_rol",
        description="Rol del usuario"
    )
    status: str = Field(
        default="activo",
        description="Estado del usuario: activo/inactivo"
    )