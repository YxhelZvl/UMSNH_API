# src/app/features/user/presentation/schemas/user_schemas.py
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from src.app.shared.schemas.generic_response import GenericResponse

# Request Schemas
class UserCreateRequest(BaseModel):
    """Schema para crear un usuario (input del API)"""
    nombre: str = Field(..., min_length=3, max_length=40, description="Nombre del usuario")
    apellidoP: str = Field(..., min_length=1, max_length=40, description="Apellido paterno")
    apellidoM: str = Field(..., min_length=1, max_length=40, description="Apellido materno")
    matricula: str = Field(..., min_length=1, max_length=15, description="Matrícula del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    contraseña: str = Field(..., min_length=6, description="Contraseña del usuario")
    id_rol: int = Field(..., description="ID del rol del usuario")

class UserUpdateRequest(BaseModel):
    """Schema para actualizar un usuario (input del API)"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=40, description="Nombre del usuario")
    apellidoP: Optional[str] = Field(None, min_length=1, max_length=40, description="Apellido paterno")
    apellidoM: Optional[str] = Field(None, min_length=1, max_length=40, description="Apellido materno")
    matricula: Optional[str] = Field(None, min_length=1, max_length=15, description="Matrícula del usuario")
    email: Optional[EmailStr] = Field(None, description="Email del usuario")
    contraseña: Optional[str] = Field(None, min_length=6, description="Contraseña del usuario")
    id_rol: Optional[int] = Field(None, description="ID del rol del usuario")
    status: Optional[bool] = Field(None, description="Estado del usuario")

# Response Schema
class UserResponse(BaseModel):
    """Schema para respuesta de usuario (output del API)"""
    id_usuario: int
    nombre: str
    apellidoP: str
    apellidoM: str
    matricula: str
    email: str
    id_rol: int
    status: bool

    class Config:
        from_attributes = True

# Generic Responses
UsersListResponse = GenericResponse[List[UserResponse]]
UserSingleResponse = GenericResponse[UserResponse]
UserDeleteResponse = GenericResponse[None]

# Schema para autenticación
class UserLoginRequest(BaseModel):
    email: EmailStr
    contraseña: str

class UserLoginResponse(BaseModel):
    id_usuario: int
    nombre: str
    email: str
    id_rol: int

class UserLoginGenericResponse(GenericResponse[UserLoginResponse]):
    pass