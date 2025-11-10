# src/app/features/administrativo/presentation/routers/administrativo_router.py
from fastapi import APIRouter, Depends
from typing import Annotated, List
from src.app.features.administrativo.application.services.administrativo_service import AdministrativoService
from src.app.features.administrativo.application.dtos import CreateAdministrativoDTO, UpdateAdministrativoDTO
from src.app.features.administrativo.infrastructure.dependencies import administrativo_service_dep
from src.app.features.administrativo.presentation.schemas.administrativo_schemas import (
    AdministrativoCreateRequest,
    AdministrativoUpdateRequest,
    AdministrativoResponse,
    AdministrativosListResponse,
    AdministrativoSingleResponse,
    AdministrativoDeleteResponse,
    AdministrativoDetailResponse,
    AdministrativoDetailSingleResponse,
    AdministrativosDetailListResponse,
    UsuarioBasicResponse
)
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/administrativos", tags=["administrativos"])

# Endpoints básicos (solo datos de administrativo)
@router.get("/", response_model=AdministrativosListResponse)
def get_all_administrativos(service: administrativo_service_dep):
    try:
        administrativos = service.get_all()
        
        administrativos_response = [
            AdministrativoResponse(
                id_administrativo=admin.id_administrativo,
                id_usuario=admin.id_usuario,
                departamento=admin.departamento
            ) for admin in administrativos
        ]
        
        return GenericResponse.create_success(
            message="Administrativos obtenidos exitosamente",
            data=administrativos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener administrativos",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_administrativo}", response_model=AdministrativoSingleResponse)
def get_administrativo_by_id(id_administrativo: int, service: administrativo_service_dep):
    try:
        administrativo = service.get_by_id(id_administrativo)
        if not administrativo:
            return GenericResponse.create_error(
                message="Administrativo no encontrado",
                errors=[f"Administrativo con ID {id_administrativo} no existe"],
                status=404
            )
        
        administrativo_response = AdministrativoResponse(
            id_administrativo=administrativo.id_administrativo,
            id_usuario=administrativo.id_usuario,
            departamento=administrativo.departamento
        )
        
        return GenericResponse.create_success(
            message="Administrativo obtenido exitosamente",
            data=administrativo_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener administrativo",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=AdministrativoSingleResponse, status_code=201)
def create_administrativo(administrativo_request: AdministrativoCreateRequest, service: administrativo_service_dep):
    try:
        create_dto = CreateAdministrativoDTO(
            id_usuario=administrativo_request.id_usuario,
            departamento=administrativo_request.departamento
        )
        
        administrativo_entity = service.create(create_dto)
        
        administrativo_response = AdministrativoResponse(
            id_administrativo=administrativo_entity.id_administrativo,
            id_usuario=administrativo_entity.id_usuario,
            departamento=administrativo_entity.departamento
        )
        
        return GenericResponse.create_success(
            message="Administrativo creado exitosamente",
            data=administrativo_response,
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
            message="Error al crear administrativo",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_administrativo}", response_model=AdministrativoSingleResponse)
def update_administrativo(id_administrativo: int, administrativo_request: AdministrativoUpdateRequest, service: administrativo_service_dep):
    try:
        update_dto = UpdateAdministrativoDTO(
            departamento=administrativo_request.departamento
        )
        
        administrativo_entity = service.update(id_administrativo, update_dto)
        
        if not administrativo_entity:
            return GenericResponse.create_error(
                message="Administrativo no encontrado",
                errors=[f"Administrativo con ID {id_administrativo} no existe"],
                status=404
            )
        
        administrativo_response = AdministrativoResponse(
            id_administrativo=administrativo_entity.id_administrativo,
            id_usuario=administrativo_entity.id_usuario,
            departamento=administrativo_entity.departamento
        )
        
        return GenericResponse.create_success(
            message="Administrativo actualizado exitosamente",
            data=administrativo_response,
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
            message="Error al actualizar administrativo",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_administrativo}", response_model=AdministrativoDeleteResponse)
def delete_administrativo(id_administrativo: int, service: administrativo_service_dep):
    try:
        success = service.delete(id_administrativo)
        
        if not success:
            return GenericResponse.create_error(
                message="Administrativo no encontrado",
                errors=[f"Administrativo con ID {id_administrativo} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Administrativo eliminado exitosamente",
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
            message="Error al eliminar administrativo",
            errors=[str(e)],
            status=500
        )

@router.get("/usuario/{id_usuario}", response_model=AdministrativoSingleResponse)
def get_administrativo_by_usuario_id(id_usuario: int, service: administrativo_service_dep):
    try:
        administrativo = service.get_by_usuario_id(id_usuario)
        if not administrativo:
            return GenericResponse.create_error(
                message="Administrativo no encontrado",
                errors=[f"Administrativo para el usuario con ID {id_usuario} no existe"],
                status=404
            )
        
        administrativo_response = AdministrativoResponse(
            id_administrativo=administrativo.id_administrativo,
            id_usuario=administrativo.id_usuario,
            departamento=administrativo.departamento
        )
        
        return GenericResponse.create_success(
            message="Administrativo obtenido exitosamente",
            data=administrativo_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener administrativo",
            errors=[str(e)],
            status=500
        )

@router.get("/departamento/{departamento}", response_model=AdministrativosListResponse)
def get_administrativos_by_departamento(departamento: str, service: administrativo_service_dep):
    try:
        administrativos = service.get_by_departamento(departamento)
        
        administrativos_response = [
            AdministrativoResponse(
                id_administrativo=admin.id_administrativo,
                id_usuario=admin.id_usuario,
                departamento=admin.departamento
            ) for admin in administrativos
        ]
        
        return GenericResponse.create_success(
            message="Administrativos obtenidos exitosamente",
            data=administrativos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener administrativos",
            errors=[str(e)],
            status=500
        )

# Endpoints detallados (con información de usuario)
@router.get("/detalles/", response_model=AdministrativosDetailListResponse)
def get_all_administrativos_detalles(service: administrativo_service_dep):
    try:
        administrativos_detallados = service.get_all_with_details()
        
        administrativos_response = [
            AdministrativoDetailResponse(
                id_administrativo=detalle['administrativo'].id_administrativo,
                usuario=UsuarioBasicResponse(
                    id_usuario=detalle['usuario'].id_usuario,
                    nombre=detalle['usuario'].nombre,
                    apellidoP=detalle['usuario'].apellidoP,
                    apellidoM=detalle['usuario'].apellidoM,
                    matricula=detalle['usuario'].matricula,
                    email=detalle['usuario'].email,
                    id_rol=detalle['usuario'].id_rol,
                    status=detalle['usuario'].status
                ),
                departamento=detalle['administrativo'].departamento
            ) for detalle in administrativos_detallados
        ]
        
        return GenericResponse.create_success(
            message="Administrativos obtenidos exitosamente con detalles",
            data=administrativos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener administrativos con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_administrativo}/detalles", response_model=AdministrativoDetailSingleResponse)
def get_administrativo_detalles_by_id(id_administrativo: int, service: administrativo_service_dep):
    try:
        administrativo_detallado = service.get_by_id_with_details(id_administrativo)
        if not administrativo_detallado:
            return GenericResponse.create_error(
                message="Administrativo no encontrado",
                errors=[f"Administrativo con ID {id_administrativo} no existe"],
                status=404
            )
        
        administrativo_response = AdministrativoDetailResponse(
            id_administrativo=administrativo_detallado['administrativo'].id_administrativo,
            usuario=UsuarioBasicResponse(
                id_usuario=administrativo_detallado['usuario'].id_usuario,
                nombre=administrativo_detallado['usuario'].nombre,
                apellidoP=administrativo_detallado['usuario'].apellidoP,
                apellidoM=administrativo_detallado['usuario'].apellidoM,
                matricula=administrativo_detallado['usuario'].matricula,
                email=administrativo_detallado['usuario'].email,
                id_rol=administrativo_detallado['usuario'].id_rol,
                status=administrativo_detallado['usuario'].status
            ),
            departamento=administrativo_detallado['administrativo'].departamento
        )
        
        return GenericResponse.create_success(
            message="Administrativo obtenido exitosamente con detalles",
            data=administrativo_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener administrativo con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/usuario/{id_usuario}/detalles", response_model=AdministrativoDetailSingleResponse)
def get_administrativo_detalles_by_usuario_id(id_usuario: int, service: administrativo_service_dep):
    try:
        administrativo_detallado = service.get_by_usuario_id_with_details(id_usuario)
        if not administrativo_detallado:
            return GenericResponse.create_error(
                message="Administrativo no encontrado",
                errors=[f"Administrativo para el usuario con ID {id_usuario} no existe"],
                status=404
            )
        
        administrativo_response = AdministrativoDetailResponse(
            id_administrativo=administrativo_detallado['administrativo'].id_administrativo,
            usuario=UsuarioBasicResponse(
                id_usuario=administrativo_detallado['usuario'].id_usuario,
                nombre=administrativo_detallado['usuario'].nombre,
                apellidoP=administrativo_detallado['usuario'].apellidoP,
                apellidoM=administrativo_detallado['usuario'].apellidoM,
                matricula=administrativo_detallado['usuario'].matricula,
                email=administrativo_detallado['usuario'].email,
                id_rol=administrativo_detallado['usuario'].id_rol,
                status=administrativo_detallado['usuario'].status
            ),
            departamento=administrativo_detallado['administrativo'].departamento
        )
        
        return GenericResponse.create_success(
            message="Administrativo obtenido exitosamente con detalles",
            data=administrativo_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener administrativo con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/departamento/{departamento}/detalles", response_model=AdministrativosDetailListResponse)
def get_administrativos_detalles_by_departamento(departamento: str, service: administrativo_service_dep):
    try:
        administrativos_detallados = service.get_by_departamento_with_details(departamento)
        
        administrativos_response = [
            AdministrativoDetailResponse(
                id_administrativo=detalle['administrativo'].id_administrativo,
                usuario=UsuarioBasicResponse(
                    id_usuario=detalle['usuario'].id_usuario,
                    nombre=detalle['usuario'].nombre,
                    apellidoP=detalle['usuario'].apellidoP,
                    apellidoM=detalle['usuario'].apellidoM,
                    matricula=detalle['usuario'].matricula,
                    email=detalle['usuario'].email,
                    id_rol=detalle['usuario'].id_rol,
                    status=detalle['usuario'].status
                ),
                departamento=detalle['administrativo'].departamento
            ) for detalle in administrativos_detallados
        ]
        
        return GenericResponse.create_success(
            message="Administrativos obtenidos exitosamente con detalles",
            data=administrativos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener administrativos con detalles",
            errors=[str(e)],
            status=500
        )