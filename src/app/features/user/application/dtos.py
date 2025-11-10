# src/app/features/user/application/dtos.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateUserDTO(BaseModel):
    """DTO para crear un nuevo usuario"""
    nombre: str
    apellidoP: str
    apellidoM: str
    matricula: str
    email: str
    contraseña: str
    id_rol: int

class UpdateUserDTO(BaseModel):
    """DTO para actualizar un usuario existente"""
    nombre: Optional[str] = None
    apellidoP: Optional[str] = None
    apellidoM: Optional[str] = None
    matricula: Optional[str] = None
    email: Optional[str] = None
    contraseña: Optional[str] = None
    id_rol: Optional[int] = None
    status: Optional[bool] = None

class UserResponseDTO(BaseModel):
    """DTO para respuesta de usuario (opcional - si decides usarlo)"""
    id_usuario: int
    nombre: str
    apellidoP: str
    apellidoM: str
    matricula: str
    email: str
    id_rol: int
    status: bool