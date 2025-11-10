# src/app/features/laboratorios/presentation/routers/laboratorio_router.py
from fastapi import APIRouter, Depends
from typing import Annotated, List
from src.app.features.laboratorios.application.services.laboratorio_service import LaboratorioService
from src.app.features.laboratorios.application.dtos import CreateLaboratorioDTO, UpdateLaboratorioDTO
from src.app.features.laboratorios.infrastructure.dependencies import laboratorio_service_dep
from src.app.features.laboratorios.presentation.schemas.laboratorio_schemas import (
    LaboratorioCreateRequest,
    LaboratorioUpdateRequest,
    LaboratorioResponse,
    LaboratoriosListResponse,
    LaboratorioSingleResponse,
    LaboratorioDeleteResponse,
    LaboratorioDetailResponse,
    LaboratorioDetailSingleResponse,
    LaboratoriosDetailListResponse,
    UsuarioBasicResponse
)
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/laboratorios", tags=["laboratorios"])

# Endpoints básicos (solo datos de laboratorio)
@router.get("/", response_model=LaboratoriosListResponse)
def get_all_laboratorios(service: laboratorio_service_dep):
    try:
        laboratorios = service.get_all()
        
        laboratorios_response = [
            LaboratorioResponse(
                id_laboratorio=lab.id_laboratorio,
                nombre=lab.nombre.valor,
                ubicacion=lab.ubicacion.valor,
                responsable_id=lab.responsable_id
            ) for lab in laboratorios
        ]
        
        return GenericResponse.create_success(
            message="Laboratorios obtenidos exitosamente",
            data=laboratorios_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener laboratorios",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_laboratorio}", response_model=LaboratorioSingleResponse)
def get_laboratorio_by_id(id_laboratorio: int, service: laboratorio_service_dep):
    try:
        laboratorio = service.get_by_id(id_laboratorio)
        if not laboratorio:
            return GenericResponse.create_error(
                message="Laboratorio no encontrado",
                errors=[f"Laboratorio con ID {id_laboratorio} no existe"],
                status=404
            )
        
        laboratorio_response = LaboratorioResponse(
            id_laboratorio=laboratorio.id_laboratorio,
            nombre=laboratorio.nombre.valor,
            ubicacion=laboratorio.ubicacion.valor,
            responsable_id=laboratorio.responsable_id
        )
        
        return GenericResponse.create_success(
            message="Laboratorio obtenido exitosamente",
            data=laboratorio_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener laboratorio",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=LaboratorioSingleResponse, status_code=201)
def create_laboratorio(laboratorio_request: LaboratorioCreateRequest, service: laboratorio_service_dep):
    try:
        create_dto = CreateLaboratorioDTO(
            nombre=laboratorio_request.nombre,
            ubicacion=laboratorio_request.ubicacion,
            responsable_id=laboratorio_request.responsable_id
        )
        
        laboratorio_entity = service.create(create_dto)
        
        laboratorio_response = LaboratorioResponse(
            id_laboratorio=laboratorio_entity.id_laboratorio,
            nombre=laboratorio_entity.nombre.valor,
            ubicacion=laboratorio_entity.ubicacion.valor,
            responsable_id=laboratorio_entity.responsable_id
        )
        
        return GenericResponse.create_success(
            message="Laboratorio creado exitosamente",
            data=laboratorio_response,
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
            message="Error al crear laboratorio",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_laboratorio}", response_model=LaboratorioSingleResponse)
def update_laboratorio(id_laboratorio: int, laboratorio_request: LaboratorioUpdateRequest, service: laboratorio_service_dep):
    try:
        update_dto = UpdateLaboratorioDTO(
            nombre=laboratorio_request.nombre,
            ubicacion=laboratorio_request.ubicacion,
            responsable_id=laboratorio_request.responsable_id
        )
        
        laboratorio_entity = service.update(id_laboratorio, update_dto)
        
        if not laboratorio_entity:
            return GenericResponse.create_error(
                message="Laboratorio no encontrado",
                errors=[f"Laboratorio con ID {id_laboratorio} no existe"],
                status=404
            )
        
        laboratorio_response = LaboratorioResponse(
            id_laboratorio=laboratorio_entity.id_laboratorio,
            nombre=laboratorio_entity.nombre.valor,
            ubicacion=laboratorio_entity.ubicacion.valor,
            responsable_id=laboratorio_entity.responsable_id
        )
        
        return GenericResponse.create_success(
            message="Laboratorio actualizado exitosamente",
            data=laboratorio_response,
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
            message="Error al actualizar laboratorio",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_laboratorio}", response_model=LaboratorioDeleteResponse)
def delete_laboratorio(id_laboratorio: int, service: laboratorio_service_dep):
    try:
        success = service.delete(id_laboratorio)
        
        if not success:
            return GenericResponse.create_error(
                message="Laboratorio no encontrado",
                errors=[f"Laboratorio con ID {id_laboratorio} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Laboratorio eliminado exitosamente",
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
            message="Error al eliminar laboratorio",
            errors=[str(e)],
            status=500
        )

@router.get("/nombre/{nombre}", response_model=LaboratorioSingleResponse)
def get_laboratorio_by_nombre(nombre: str, service: laboratorio_service_dep):
    try:
        laboratorio = service.get_by_nombre(nombre)
        if not laboratorio:
            return GenericResponse.create_error(
                message="Laboratorio no encontrado",
                errors=[f"Laboratorio con nombre {nombre} no existe"],
                status=404
            )
        
        laboratorio_response = LaboratorioResponse(
            id_laboratorio=laboratorio.id_laboratorio,
            nombre=laboratorio.nombre.valor,
            ubicacion=laboratorio.ubicacion.valor,
            responsable_id=laboratorio.responsable_id
        )
        
        return GenericResponse.create_success(
            message="Laboratorio obtenido exitosamente",
            data=laboratorio_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener laboratorio",
            errors=[str(e)],
            status=500
        )

@router.get("/responsable/{responsable_id}", response_model=LaboratoriosListResponse)
def get_laboratorios_by_responsable(responsable_id: int, service: laboratorio_service_dep):
    try:
        laboratorios = service.get_by_responsable(responsable_id)
        
        laboratorios_response = [
            LaboratorioResponse(
                id_laboratorio=lab.id_laboratorio,
                nombre=lab.nombre.valor,
                ubicacion=lab.ubicacion.valor,
                responsable_id=lab.responsable_id
            ) for lab in laboratorios
        ]
        
        return GenericResponse.create_success(
            message="Laboratorios obtenidos exitosamente",
            data=laboratorios_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener laboratorios",
            errors=[str(e)],
            status=500
        )

# Endpoints detallados (con información del responsable)
@router.get("/detalles/", response_model=LaboratoriosDetailListResponse)
def get_all_laboratorios_detalles(service: laboratorio_service_dep):
    try:
        laboratorios_detallados = service.get_all_with_details()
        
        laboratorios_response = []
        for detalle in laboratorios_detallados:
            laboratorio_db = detalle['laboratorio']
            responsable_db = detalle['responsable']
            
            # Construir respuesta del responsable si existe
            responsable_response = None
            if responsable_db:
                responsable_response = UsuarioBasicResponse(
                    id_usuario=responsable_db.id_usuario,
                    nombre=responsable_db.nombre,
                    apellidoP=responsable_db.apellidoP,
                    apellidoM=responsable_db.apellidoM,
                    matricula=responsable_db.matricula,
                    email=responsable_db.email,
                    id_rol=responsable_db.id_rol,
                    status=responsable_db.status
                )
            
            laboratorio_detail = LaboratorioDetailResponse(
                id_laboratorio=laboratorio_db.id_laboratorio,
                nombre=laboratorio_db.nombre,
                ubicacion=laboratorio_db.ubicacion,
                responsable=responsable_response
            )
            laboratorios_response.append(laboratorio_detail)
        
        return GenericResponse.create_success(
            message="Laboratorios obtenidos exitosamente con detalles",
            data=laboratorios_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener laboratorios con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_laboratorio}/detalles", response_model=LaboratorioDetailSingleResponse)
def get_laboratorio_detalles_by_id(id_laboratorio: int, service: laboratorio_service_dep):
    try:
        laboratorio_detallado = service.get_by_id_with_details(id_laboratorio)
        if not laboratorio_detallado:
            return GenericResponse.create_error(
                message="Laboratorio no encontrado",
                errors=[f"Laboratorio con ID {id_laboratorio} no existe"],
                status=404
            )
        
        laboratorio_db = laboratorio_detallado['laboratorio']
        responsable_db = laboratorio_detallado['responsable']
        
        # Construir respuesta del responsable si existe
        responsable_response = None
        if responsable_db:
            responsable_response = UsuarioBasicResponse(
                id_usuario=responsable_db.id_usuario,
                nombre=responsable_db.nombre,
                apellidoP=responsable_db.apellidoP,
                apellidoM=responsable_db.apellidoM,
                matricula=responsable_db.matricula,
                email=responsable_db.email,
                id_rol=responsable_db.id_rol,
                status=responsable_db.status
            )
        
        laboratorio_response = LaboratorioDetailResponse(
            id_laboratorio=laboratorio_db.id_laboratorio,
            nombre=laboratorio_db.nombre,
            ubicacion=laboratorio_db.ubicacion,
            responsable=responsable_response
        )
        
        return GenericResponse.create_success(
            message="Laboratorio obtenido exitosamente con detalles",
            data=laboratorio_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener laboratorio con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/responsable/{responsable_id}/detalles", response_model=LaboratoriosDetailListResponse)
def get_laboratorios_detalles_by_responsable(responsable_id: int, service: laboratorio_service_dep):
    try:
        laboratorios_detallados = service.get_by_responsable_with_details(responsable_id)
        
        laboratorios_response = []
        for detalle in laboratorios_detallados:
            laboratorio_db = detalle['laboratorio']
            responsable_db = detalle['responsable']
            
            # Construir respuesta del responsable (debería existir en este caso)
            responsable_response = UsuarioBasicResponse(
                id_usuario=responsable_db.id_usuario,
                nombre=responsable_db.nombre,
                apellidoP=responsable_db.apellidoP,
                apellidoM=responsable_db.apellidoM,
                matricula=responsable_db.matricula,
                email=responsable_db.email,
                id_rol=responsable_db.id_rol,
                status=responsable_db.status
            ) if responsable_db else None
            
            laboratorio_detail = LaboratorioDetailResponse(
                id_laboratorio=laboratorio_db.id_laboratorio,
                nombre=laboratorio_db.nombre,
                ubicacion=laboratorio_db.ubicacion,
                responsable=responsable_response
            )
            laboratorios_response.append(laboratorio_detail)
        
        return GenericResponse.create_success(
            message="Laboratorios obtenidos exitosamente con detalles",
            data=laboratorios_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener laboratorios con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/nombre/{nombre}/detalles", response_model=LaboratorioDetailSingleResponse)
def get_laboratorio_detalles_by_nombre(nombre: str, service: laboratorio_service_dep):
    try:
        laboratorio_detallado = service.get_by_nombre_with_details(nombre)
        if not laboratorio_detallado:
            return GenericResponse.create_error(
                message="Laboratorio no encontrado",
                errors=[f"Laboratorio con nombre {nombre} no existe"],
                status=404
            )
        
        laboratorio_db = laboratorio_detallado['laboratorio']
        responsable_db = laboratorio_detallado['responsable']
        
        # Construir respuesta del responsable si existe
        responsable_response = None
        if responsable_db:
            responsable_response = UsuarioBasicResponse(
                id_usuario=responsable_db.id_usuario,
                nombre=responsable_db.nombre,
                apellidoP=responsable_db.apellidoP,
                apellidoM=responsable_db.apellidoM,
                matricula=responsable_db.matricula,
                email=responsable_db.email,
                id_rol=responsable_db.id_rol,
                status=responsable_db.status
            )
        
        laboratorio_response = LaboratorioDetailResponse(
            id_laboratorio=laboratorio_db.id_laboratorio,
            nombre=laboratorio_db.nombre,
            ubicacion=laboratorio_db.ubicacion,
            responsable=responsable_response
        )
        
        return GenericResponse.create_success(
            message="Laboratorio obtenido exitosamente con detalles",
            data=laboratorio_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener laboratorio con detalles",
            errors=[str(e)],
            status=500
        )