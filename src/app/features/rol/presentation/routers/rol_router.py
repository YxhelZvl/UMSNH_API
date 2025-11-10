# src/app/features/rol/presentation/routers/rol_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from src.app.features.rol.application.services.rol_service import RolService
from src.app.features.rol.application.dtos import CreateRolDTO, UpdateRolDTO
from src.app.features.rol.infrastructure.dependencies import rol_service_dep
from src.app.features.rol.presentation.schemas.rol_schemas import (
    RolCreateRequest,
    RolUpdateRequest, 
    RolResponse,
    RolesListResponse,
    RolSingleResponse,
    RolDeleteResponse
)
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/", response_model=RolesListResponse)
def get_all_roles(service: rol_service_dep):
    """Obtener todos los roles"""
    try:
        roles = service.get_all()
        
        # Convertir entidades de dominio a schemas de respuesta
        roles_response = [
            RolResponse(
                id_rol=rol.id_rol,
                tipo_rol=rol.tipo_rol.valor  # Extraer string del Value Object
            ) for rol in roles
        ]
        
        return GenericResponse.create_success(
            message="Roles obtenidos exitosamente",
            data=roles_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener roles",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_rol}", response_model=RolSingleResponse)
def get_rol_by_id(id_rol: int, service: rol_service_dep):
    """Obtener un rol por ID"""
    try:
        rol = service.get_by_id(id_rol)
        if not rol:
            return GenericResponse.create_error(
                message="Rol no encontrado",
                errors=[f"Rol con ID {id_rol} no existe"],
                status=404
            )
        
        rol_response = RolResponse(
            id_rol=rol.id_rol,
            tipo_rol=rol.tipo_rol.valor
        )
        
        return GenericResponse.create_success(
            message="Rol obtenido exitosamente",
            data=rol_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener rol",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=RolSingleResponse, status_code=201)
def create_rol(rol_request: RolCreateRequest, service: rol_service_dep):
    """Crear un nuevo rol"""
    try:
        # Convertir schema de request a DTO de aplicación
        create_dto = CreateRolDTO(tipo_rol=rol_request.tipo_rol)
        
        # Llamar al servicio
        rol_entity = service.create(create_dto)
        
        # Convertir entidad a schema de respuesta
        rol_response = RolResponse(
            id_rol=rol_entity.id_rol,
            tipo_rol=rol_entity.tipo_rol.valor
        )
        
        return GenericResponse.create_success(
            message="Rol creado exitosamente",
            data=rol_response,
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
            message="Error al crear rol",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_rol}", response_model=RolSingleResponse)
def update_rol(id_rol: int, rol_request: RolUpdateRequest, service: rol_service_dep):
    """Actualizar un rol existente"""
    try:
        # Convertir schema de request a DTO de aplicación
        update_dto = UpdateRolDTO(tipo_rol=rol_request.tipo_rol)
        
        # Llamar al servicio
        rol_entity = service.update(id_rol, update_dto)
        
        if not rol_entity:
            return GenericResponse.create_error(
                message="Rol no encontrado",
                errors=[f"Rol con ID {id_rol} no existe"],
                status=404
            )
        
        # Convertir entidad a schema de respuesta
        rol_response = RolResponse(
            id_rol=rol_entity.id_rol,
            tipo_rol=rol_entity.tipo_rol.valor
        )
        
        return GenericResponse.create_success(
            message="Rol actualizado exitosamente",
            data=rol_response,
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
            message="Error al actualizar rol",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_rol}", response_model=RolDeleteResponse)
def delete_rol(id_rol: int, service: rol_service_dep):
    """Eliminar un rol"""
    try:
        success = service.delete(id_rol)
        
        if not success:
            return GenericResponse.create_error(
                message="Rol no encontrado",
                errors=[f"Rol con ID {id_rol} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Rol eliminado exitosamente",
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
            message="Error al eliminar rol",
            errors=[str(e)],
            status=500
        )

@router.get("/tipo/{tipo_rol}", response_model=RolSingleResponse)
def get_rol_by_tipo(tipo_rol: str, service: rol_service_dep):
    """Obtener un rol por tipo"""
    try:
        rol = service.get_by_tipo(tipo_rol)
        if not rol:
            return GenericResponse.create_error(
                message="Rol no encontrado",
                errors=[f"Rol con tipo '{tipo_rol}' no existe"],
                status=404
            )
        
        rol_response = RolResponse(
            id_rol=rol.id_rol,
            tipo_rol=rol.tipo_rol.valor
        )
        
        return GenericResponse.create_success(
            message="Rol obtenido exitosamente",
            data=rol_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener rol",
            errors=[str(e)],
            status=500
        )