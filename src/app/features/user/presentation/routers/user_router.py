# src/app/features/user/presentation/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from src.app.features.user.application.services.user_service import UserService
from src.app.features.user.application.dtos import CreateUserDTO, UpdateUserDTO
from src.app.features.user.infrastructure.dependencies import user_service_dep
from src.app.shared.schemas.generic_response import GenericResponse
from src.app.features.user.presentation.schemas.user_schemas import (
    UserCreateRequest,
    UserUpdateRequest,
    UserResponse,
    UsersListResponse,
    UserSingleResponse,
    UserDeleteResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserLoginGenericResponse,
    UserDetailResponse,
    UsersDetailsListResponse
)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=UsersListResponse)
def get_all_users(service: user_service_dep):
    """Obtener todos los usuarios"""
    try:
        users = service.get_all()
        
        # Convertir entidades de dominio a schemas de respuesta
        users_response = [
            UserResponse(
                id_usuario=user.id_usuario,
                nombre=user.nombre.valor,
                apellidoP=user.apellidoP,
                apellidoM=user.apellidoM,
                matricula=user.matricula.valor,
                email=user.email.valor,
                id_rol=user.id_rol,
                status=user.status
            ) for user in users
        ]
        
        return GenericResponse.create_success(
            message="Usuarios obtenidos exitosamente",
            data=users_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener usuarios",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_usuario}", response_model=UserSingleResponse)
def get_user_by_id(id_usuario: int, service: user_service_dep):
    """Obtener un usuario por ID"""
    try:
        user = service.get_by_id(id_usuario)
        if not user:
            return GenericResponse.create_error(
                message="Usuario no encontrado",
                errors=[f"Usuario con ID {id_usuario} no existe"],
                status=404
            )
        
        user_response = UserResponse(
            id_usuario=user.id_usuario,
            nombre=user.nombre.valor,
            apellidoP=user.apellidoP,
            apellidoM=user.apellidoM,
            matricula=user.matricula.valor,
            email=user.email.valor,
            id_rol=user.id_rol,
            status=user.status
        )
        
        return GenericResponse.create_success(
            message="Usuario obtenido exitosamente",
            data=user_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener usuario",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=UserSingleResponse, status_code=201)
def create_user(user_request: UserCreateRequest, service: user_service_dep):
    """Crear un nuevo usuario"""
    try:
        # Convertir schema de request a DTO de aplicación
        create_dto = CreateUserDTO(
            nombre=user_request.nombre,
            apellidoP=user_request.apellidoP,
            apellidoM=user_request.apellidoM,
            matricula=user_request.matricula,
            email=user_request.email,
            contraseña=user_request.contraseña,
            id_rol=user_request.id_rol
        )
        
        # Llamar al servicio
        user_entity = service.create(create_dto)
        
        # Convertir entidad a schema de respuesta
        user_response = UserResponse(
            id_usuario=user_entity.id_usuario,
            nombre=user_entity.nombre.valor,
            apellidoP=user_entity.apellidoP,
            apellidoM=user_entity.apellidoM,
            matricula=user_entity.matricula.valor,
            email=user_entity.email.valor,
            id_rol=user_entity.id_rol,
            status=user_entity.status
        )
        
        return GenericResponse.create_success(
            message="Usuario creado exitosamente",
            data=user_response,
            status=201
        )
        
    except ValueError as e:
        # Errores de negocio (validaciones, duplicados, etc.)
        return GenericResponse.create_error(
            message="Error de validación",
            errors=[str(e)],
            status=400
        )
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al crear usuario",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_usuario}", response_model=UserSingleResponse)
def update_user(id_usuario: int, user_request: UserUpdateRequest, service: user_service_dep):
    """Actualizar un usuario existente"""
    try:
        # Convertir schema de request a DTO de aplicación
        update_dto = UpdateUserDTO(
            nombre=user_request.nombre,
            apellidoP=user_request.apellidoP,
            apellidoM=user_request.apellidoM,
            matricula=user_request.matricula,
            email=user_request.email,
            contraseña=user_request.contraseña,
            id_rol=user_request.id_rol,
            status=user_request.status
        )
        
        # Llamar al servicio
        user_entity = service.update(id_usuario, update_dto)
        
        if not user_entity:
            return GenericResponse.create_error(
                message="Usuario no encontrado",
                errors=[f"Usuario con ID {id_usuario} no existe"],
                status=404
            )
        
        # Convertir entidad a schema de respuesta
        user_response = UserResponse(
            id_usuario=user_entity.id_usuario,
            nombre=user_entity.nombre.valor,
            apellidoP=user_entity.apellidoP,
            apellidoM=user_entity.apellidoM,
            matricula=user_entity.matricula.valor,
            email=user_entity.email.valor,
            id_rol=user_entity.id_rol,
            status=user_entity.status
        )
        
        return GenericResponse.create_success(
            message="Usuario actualizado exitosamente",
            data=user_response,
            status=200
        )
        
    except ValueError as e:
        return GenericResponse.create_error(
            message="Error de validación",
            errors=[str(e)],
            status=400
        )
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al actualizar usuario",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_usuario}", response_model=UserDeleteResponse)
def delete_user(id_usuario: int, service: user_service_dep):
    """Eliminar un usuario (lógico: desactivar)"""
    try:
        success = service.delete(id_usuario)
        
        if not success:
            return GenericResponse.create_error(
                message="Usuario no encontrado",
                errors=[f"Usuario con ID {id_usuario} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Usuario eliminado (desactivado) exitosamente",
            data=None,
            status=200
        )
        
    except ValueError as e:
        return GenericResponse.create_error(
            message="Error de validación",
            errors=[str(e)],
            status=400
        )
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al eliminar usuario",
            errors=[str(e)],
            status=500
        )

@router.get("/email/{email}", response_model=UserSingleResponse)
def get_user_by_email(email: str, service: user_service_dep):
    """Obtener un usuario por email"""
    try:
        user = service.get_by_email(email)
        if not user:
            return GenericResponse.create_error(
                message="Usuario no encontrado",
                errors=[f"Usuario con email {email} no existe"],
                status=404
            )
        
        user_response = UserResponse(
            id_usuario=user.id_usuario,
            nombre=user.nombre.valor,
            apellidoP=user.apellidoP,
            apellidoM=user.apellidoM,
            matricula=user.matricula.valor,
            email=user.email.valor,
            id_rol=user.id_rol,
            status=user.status
        )
        
        return GenericResponse.create_success(
            message="Usuario obtenido exitosamente",
            data=user_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener usuario",
            errors=[str(e)],
            status=500
        )

@router.get("/matricula/{matricula}", response_model=UserSingleResponse)
def get_user_by_matricula(matricula: str, service: user_service_dep):
    """Obtener un usuario por matrícula"""
    try:
        user = service.get_by_matricula(matricula)
        if not user:
            return GenericResponse.create_error(
                message="Usuario no encontrado",
                errors=[f"Usuario con matrícula {matricula} no existe"],
                status=404
            )
        
        user_response = UserResponse(
            id_usuario=user.id_usuario,
            nombre=user.nombre.valor,
            apellidoP=user.apellidoP,
            apellidoM=user.apellidoM,
            matricula=user.matricula.valor,
            email=user.email.valor,
            id_rol=user.id_rol,
            status=user.status
        )
        
        return GenericResponse.create_success(
            message="Usuario obtenido exitosamente",
            data=user_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener usuario",
            errors=[str(e)],
            status=500
        )

@router.get("/rol/{id_rol}", response_model=UsersListResponse)
def get_users_by_rol(id_rol: int, service: user_service_dep):
    """Obtener usuarios por rol"""
    try:
        users = service.get_by_rol(id_rol)
        
        users_response = [
            UserResponse(
                id_usuario=user.id_usuario,
                nombre=user.nombre.valor,
                apellidoP=user.apellidoP,
                apellidoM=user.apellidoM,
                matricula=user.matricula.valor,
                email=user.email.valor,
                id_rol=user.id_rol,
                status=user.status
            ) for user in users
        ]
        
        return GenericResponse.create_success(
            message="Usuarios obtenidos exitosamente",
            data=users_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener usuarios por rol",
            errors=[str(e)],
            status=500
        )

@router.post("/login", response_model=UserLoginGenericResponse)
def login_user(login_request: UserLoginRequest, service: user_service_dep):
    """Autenticar usuario"""
    try:
        user = service.authenticate(login_request.email, login_request.contraseña)
        if not user:
            return GenericResponse.create_error(
                message="Credenciales inválidas",
                errors=["Email o contraseña incorrectos"],
                status=401
            )
        
        user_response = UserLoginResponse(
            id_usuario=user.id_usuario,
            nombre=user.nombre.valor,
            email=user.email.valor,
            id_rol=user.id_rol
        )
        
        return GenericResponse.create_success(
            message="Login exitoso",
            data=user_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error en el login",
            errors=[str(e)],
            status=500
        )
        
@router.get("/detalles/", response_model=UsersDetailsListResponse)
def get_user_details_with_details(service: user_service_dep):
    """Obtener todos los usuarios con detalles de rol"""
    try:
        users = service.get_all_users_with_details()
        
        users_response = [
            UserDetailResponse(
                id_usuario=user['usuario'].id_usuario,
                nombre=user['usuario'].nombre,
                apellidoP=user['usuario'].apellidoP,
                apellidoM=user['usuario'].apellidoM,
                matricula=user['usuario'].matricula,
                email=user['usuario'].email,
                id_rol=user['usuario'].id_rol,
                rol_tipo=user['rol'].tipo_rol,
                status=user['usuario'].status
            ) for user in users
        ]
        
        return GenericResponse.create_success(
            message="Usuarios con detalles obtenidos exitosamente",
            data=users_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener usuarios con detalles",
            errors=[str(e)],
            status=500
        )