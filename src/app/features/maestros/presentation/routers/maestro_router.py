# src/app/features/maestros/presentation/routers/maestro_router.py
from fastapi import APIRouter, Depends
from typing import Annotated, List
from src.app.features.maestros.application.services.maestro_service import MaestroService
from src.app.features.maestros.application.dtos import CreateMaestroDTO, UpdateMaestroDTO
from src.app.features.maestros.infrastructure.dependencies import maestro_service_dep
from src.app.features.maestros.presentation.schemas.maestro_schemas import (
    MaestroCreateRequest,
    MaestroUpdateRequest,
    MaestroResponse,
    MaestrosListResponse,
    MaestroSingleResponse,
    MaestroDeleteResponse,
    MaestroDetailResponse,
    MaestroDetailSingleResponse,
    MaestrosDetailListResponse,
    UsuarioBasicResponse
)
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/maestros", tags=["maestros"])

# Endpoints básicos (solo datos de maestro)
@router.get("/", response_model=MaestrosListResponse)
def get_all_maestros(service: maestro_service_dep):
    try:
        maestros = service.get_all()
        
        maestros_response = [
            MaestroResponse(
                id_maestro=maestro.id_maestro,
                id_usuario=maestro.id_usuario
            ) for maestro in maestros
        ]
        
        return GenericResponse.create_success(
            message="Maestros obtenidos exitosamente",
            data=maestros_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener maestros",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_maestro}", response_model=MaestroSingleResponse)
def get_maestro_by_id(id_maestro: int, service: maestro_service_dep):
    try:
        maestro = service.get_by_id(id_maestro)
        if not maestro:
            return GenericResponse.create_error(
                message="Maestro no encontrado",
                errors=[f"Maestro con ID {id_maestro} no existe"],
                status=404
            )
        
        maestro_response = MaestroResponse(
            id_maestro=maestro.id_maestro,
            id_usuario=maestro.id_usuario
        )
        
        return GenericResponse.create_success(
            message="Maestro obtenido exitosamente",
            data=maestro_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener maestro",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=MaestroSingleResponse, status_code=201)
def create_maestro(maestro_request: MaestroCreateRequest, service: maestro_service_dep):
    try:
        create_dto = CreateMaestroDTO(
            id_usuario=maestro_request.id_usuario
        )
        
        maestro_entity = service.create(create_dto)
        
        maestro_response = MaestroResponse(
            id_maestro=maestro_entity.id_maestro,
            id_usuario=maestro_entity.id_usuario
        )
        
        return GenericResponse.create_success(
            message="Maestro creado exitosamente",
            data=maestro_response,
            status=201
        )
        
    except ValueError as e:
        return GenericResponse.create_error(
            message="Error de validación",
            errors=[str(e)],
            status=400
        )
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al crear maestro",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_maestro}", response_model=MaestroSingleResponse)
def update_maestro(id_maestro: int, maestro_request: MaestroUpdateRequest, service: maestro_service_dep):
    try:
        update_dto = UpdateMaestroDTO()
        
        maestro_entity = service.update(id_maestro, update_dto)
        
        if not maestro_entity:
            return GenericResponse.create_error(
                message="Maestro no encontrado",
                errors=[f"Maestro con ID {id_maestro} no existe"],
                status=404
            )
        
        maestro_response = MaestroResponse(
            id_maestro=maestro_entity.id_maestro,
            id_usuario=maestro_entity.id_usuario
        )
        
        return GenericResponse.create_success(
            message="Maestro actualizado exitosamente",
            data=maestro_response,
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
            message="Error al actualizar maestro",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_maestro}", response_model=MaestroDeleteResponse)
def delete_maestro(id_maestro: int, service: maestro_service_dep):
    try:
        success = service.delete(id_maestro)
        
        if not success:
            return GenericResponse.create_error(
                message="Maestro no encontrado",
                errors=[f"Maestro con ID {id_maestro} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Maestro eliminado exitosamente",
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
            message="Error al eliminar maestro",
            errors=[str(e)],
            status=500
        )

@router.get("/usuario/{id_usuario}", response_model=MaestroSingleResponse)
def get_maestro_by_usuario_id(id_usuario: int, service: maestro_service_dep):
    try:
        maestro = service.get_by_usuario_id(id_usuario)
        if not maestro:
            return GenericResponse.create_error(
                message="Maestro no encontrado",
                errors=[f"Maestro para el usuario con ID {id_usuario} no existe"],
                status=404
            )
        
        maestro_response = MaestroResponse(
            id_maestro=maestro.id_maestro,
            id_usuario=maestro.id_usuario
        )
        
        return GenericResponse.create_success(
            message="Maestro obtenido exitosamente",
            data=maestro_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener maestro",
            errors=[str(e)],
            status=500
        )

# Endpoints detallados (con información de usuario)
@router.get("/detalles/", response_model=MaestrosDetailListResponse)
def get_all_maestros_detalles(service: maestro_service_dep):
    try:
        maestros_detallados = service.get_all_with_details()
        
        maestros_response = [
            MaestroDetailResponse(
                id_maestro=detalle['maestro'].id_maestro,
                usuario=UsuarioBasicResponse(
                    id_usuario=detalle['usuario'].id_usuario,
                    nombre=detalle['usuario'].nombre,
                    apellidoP=detalle['usuario'].apellidoP,
                    apellidoM=detalle['usuario'].apellidoM,
                    matricula=detalle['usuario'].matricula,
                    email=detalle['usuario'].email,
                    id_rol=detalle['usuario'].id_rol,
                    status=detalle['usuario'].status
                )
            ) for detalle in maestros_detallados
        ]
        
        return GenericResponse.create_success(
            message="Maestros obtenidos exitosamente con detalles",
            data=maestros_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener maestros con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_maestro}/detalles", response_model=MaestroDetailSingleResponse)
def get_maestro_detalles_by_id(id_maestro: int, service: maestro_service_dep):
    try:
        maestro_detallado = service.get_by_id_with_details(id_maestro)
        if not maestro_detallado:
            return GenericResponse.create_error(
                message="Maestro no encontrado",
                errors=[f"Maestro con ID {id_maestro} no existe"],
                status=404
            )
        
        maestro_response = MaestroDetailResponse(
            id_maestro=maestro_detallado['maestro'].id_maestro,
            usuario=UsuarioBasicResponse(
                id_usuario=maestro_detallado['usuario'].id_usuario,
                nombre=maestro_detallado['usuario'].nombre,
                apellidoP=maestro_detallado['usuario'].apellidoP,
                apellidoM=maestro_detallado['usuario'].apellidoM,
                matricula=maestro_detallado['usuario'].matricula,
                email=maestro_detallado['usuario'].email,
                id_rol=maestro_detallado['usuario'].id_rol,
                status=maestro_detallado['usuario'].status
            )
        )
        
        return GenericResponse.create_success(
            message="Maestro obtenido exitosamente con detalles",
            data=maestro_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener maestro con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/usuario/{id_usuario}/detalles", response_model=MaestroDetailSingleResponse)
def get_maestro_detalles_by_usuario_id(id_usuario: int, service: maestro_service_dep):
    try:
        maestro_detallado = service.get_by_usuario_id_with_details(id_usuario)
        if not maestro_detallado:
            return GenericResponse.create_error(
                message="Maestro no encontrado",
                errors=[f"Maestro para el usuario con ID {id_usuario} no existe"],
                status=404
            )
        
        maestro_response = MaestroDetailResponse(
            id_maestro=maestro_detallado['maestro'].id_maestro,
            usuario=UsuarioBasicResponse(
                id_usuario=maestro_detallado['usuario'].id_usuario,
                nombre=maestro_detallado['usuario'].nombre,
                apellidoP=maestro_detallado['usuario'].apellidoP,
                apellidoM=maestro_detallado['usuario'].apellidoM,
                matricula=maestro_detallado['usuario'].matricula,
                email=maestro_detallado['usuario'].email,
                id_rol=maestro_detallado['usuario'].id_rol,
                status=maestro_detallado['usuario'].status
            )
        )
        
        return GenericResponse.create_success(
            message="Maestro obtenido exitosamente con detalles",
            data=maestro_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener maestro con detalles",
            errors=[str(e)],
            status=500
        )