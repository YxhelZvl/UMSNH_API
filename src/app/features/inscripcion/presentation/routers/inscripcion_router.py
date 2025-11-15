# src/app/features/inscripcion/presentation/routers/inscripcion_router.py
from fastapi import APIRouter, Depends
from typing import Annotated, List
from src.app.features.inscripcion.application.services.inscripcion_service import InscripcionService
from src.app.features.inscripcion.application.dtos import CreateInscripcionDTO, UpdateInscripcionDTO
from src.app.features.inscripcion.infrastructure.dependencies import inscripcion_service_dep
from src.app.features.inscripcion.presentation.schemas.inscripcion_schemas import (
    InscripcionCreateRequest,
    InscripcionUpdateRequest,
    InscripcionResponse,
    InscripcionesListResponse,
    InscripcionSingleResponse,
    InscripcionDeleteResponse
)
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])

@router.get("/", response_model=InscripcionesListResponse)
def get_all_inscripciones(service: inscripcion_service_dep):
    try:
        inscripciones = service.get_all()
        
        inscripciones_response = [
            InscripcionResponse(
                id_inscripcion=inscripcion.id_inscripcion,
                id_usuario=inscripcion.id_usuario,
                id_ciclo=inscripcion.id_ciclo,
                fecha_inscripcion=inscripcion.fecha_inscripcion,
                estado=inscripcion.estado.valor.value
            ) for inscripcion in inscripciones
        ]
        
        return GenericResponse.create_success(
            message="Inscripciones obtenidas exitosamente",
            data=inscripciones_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener inscripciones",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_inscripcion}", response_model=InscripcionSingleResponse)
def get_inscripcion_by_id(id_inscripcion: int, service: inscripcion_service_dep):
    try:
        inscripcion = service.get_by_id(id_inscripcion)
        if not inscripcion:
            return GenericResponse.create_error(
                message="Inscripción no encontrada",
                errors=[f"Inscripción con ID {id_inscripcion} no existe"],
                status=404
            )
        
        inscripcion_response = InscripcionResponse(
            id_inscripcion=inscripcion.id_inscripcion,
            id_usuario=inscripcion.id_usuario,
            id_ciclo=inscripcion.id_ciclo,
            fecha_inscripcion=inscripcion.fecha_inscripcion,
            estado=inscripcion.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Inscripción obtenida exitosamente",
            data=inscripcion_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener inscripción",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=InscripcionSingleResponse, status_code=201)
def create_inscripcion(inscripcion_request: InscripcionCreateRequest, service: inscripcion_service_dep):
    try:
        create_dto = CreateInscripcionDTO(
            id_usuario=inscripcion_request.id_usuario,
            id_ciclo=inscripcion_request.id_ciclo,
            fecha_inscripcion=inscripcion_request.fecha_inscripcion,
            estado=inscripcion_request.estado
        )
        
        inscripcion_entity = service.create(create_dto)
        
        inscripcion_response = InscripcionResponse(
            id_inscripcion=inscripcion_entity.id_inscripcion,
            id_usuario=inscripcion_entity.id_usuario,
            id_ciclo=inscripcion_entity.id_ciclo,
            fecha_inscripcion=inscripcion_entity.fecha_inscripcion,
            estado=inscripcion_entity.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Inscripción creada exitosamente",
            data=inscripcion_response,
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
            message="Error al crear inscripción",
            errors=[str(e)],
            status=500
        )

@router.post("/last_ciclo/{id_usuario}", response_model=InscripcionSingleResponse, status_code=201)
def create_last_ciclo(id_usuario: int, service: inscripcion_service_dep):
    try:
        inscripcion_entity = service.create_last_ciclo(id_usuario)
        
        inscripcion_response = InscripcionResponse(
            id_inscripcion=inscripcion_entity.id_inscripcion,
            id_usuario=inscripcion_entity.id_usuario,
            id_ciclo=inscripcion_entity.id_ciclo,
            fecha_inscripcion=inscripcion_entity.fecha_inscripcion,
            estado=inscripcion_entity.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Inscripción creada exitosamente",
            data=inscripcion_response,
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
            message="Error al crear inscripción",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_inscripcion}", response_model=InscripcionSingleResponse)
def update_inscripcion(id_inscripcion: int, inscripcion_request: InscripcionUpdateRequest, service: inscripcion_service_dep):
    try:
        update_dto = UpdateInscripcionDTO(
            estado=inscripcion_request.estado
        )
        
        inscripcion_entity = service.update(id_inscripcion, update_dto)
        
        if not inscripcion_entity:
            return GenericResponse.create_error(
                message="Inscripción no encontrada",
                errors=[f"Inscripción con ID {id_inscripcion} no existe"],
                status=404
            )
        
        inscripcion_response = InscripcionResponse(
            id_inscripcion=inscripcion_entity.id_inscripcion,
            id_usuario=inscripcion_entity.id_usuario,
            id_ciclo=inscripcion_entity.id_ciclo,
            fecha_inscripcion=inscripcion_entity.fecha_inscripcion,
            estado=inscripcion_entity.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Inscripción actualizada exitosamente",
            data=inscripcion_response,
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
            message="Error al actualizar inscripción",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_inscripcion}", response_model=InscripcionDeleteResponse)
def delete_inscripcion(id_inscripcion: int, service: inscripcion_service_dep):
    try:
        success = service.delete(id_inscripcion)
        
        if not success:
            return GenericResponse.create_error(
                message="Inscripción no encontrada",
                errors=[f"Inscripción con ID {id_inscripcion} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Inscripción eliminada exitosamente",
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
            message="Error al eliminar inscripción",
            errors=[str(e)],
            status=500
        )

@router.get("/usuario/{id_usuario}", response_model=InscripcionesListResponse)
def get_inscripciones_by_usuario_id(id_usuario: int, service: inscripcion_service_dep):
    try:
        inscripciones = service.get_by_usuario_id(id_usuario)
        
        inscripciones_response = [
            InscripcionResponse(
                id_inscripcion=inscripcion.id_inscripcion,
                id_usuario=inscripcion.id_usuario,
                id_ciclo=inscripcion.id_ciclo,
                fecha_inscripcion=inscripcion.fecha_inscripcion,
                estado=inscripcion.estado.valor.value
            ) for inscripcion in inscripciones
        ]
        
        return GenericResponse.create_success(
            message="Inscripciones obtenidas exitosamente",
            data=inscripciones_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener inscripciones",
            errors=[str(e)],
            status=500
        )

@router.get("/ciclo/{id_ciclo}", response_model=InscripcionesListResponse)
def get_inscripciones_by_ciclo_id(id_ciclo: int, service: inscripcion_service_dep):
    try:
        inscripciones = service.get_by_ciclo_id(id_ciclo)
        
        inscripciones_response = [
            InscripcionResponse(
                id_inscripcion=inscripcion.id_inscripcion,
                id_usuario=inscripcion.id_usuario,
                id_ciclo=inscripcion.id_ciclo,
                fecha_inscripcion=inscripcion.fecha_inscripcion,
                estado=inscripcion.estado.valor.value
            ) for inscripcion in inscripciones
        ]
        
        return GenericResponse.create_success(
            message="Inscripciones obtenidas exitosamente",
            data=inscripciones_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener inscripciones",
            errors=[str(e)],
            status=500
        )

@router.get("/usuario/{id_usuario}/activas", response_model=InscripcionesListResponse)
def get_inscripciones_activas_by_usuario(id_usuario: int, service: inscripcion_service_dep):
    try:
        inscripciones = service.get_inscripciones_activas_by_usuario(id_usuario)
        
        inscripciones_response = [
            InscripcionResponse(
                id_inscripcion=inscripcion.id_inscripcion,
                id_usuario=inscripcion.id_usuario,
                id_ciclo=inscripcion.id_ciclo,
                fecha_inscripcion=inscripcion.fecha_inscripcion,
                estado=inscripcion.estado.valor.value
            ) for inscripcion in inscripciones
        ]
        
        return GenericResponse.create_success(
            message="Inscripciones activas obtenidas exitosamente",
            data=inscripciones_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener inscripciones activas",
            errors=[str(e)],
            status=500
        )

@router.patch("/{id_inscripcion}/finalizar", response_model=InscripcionSingleResponse)
def finalizar_inscripcion(id_inscripcion: int, service: inscripcion_service_dep):
    try:
        inscripcion_entity = service.finalizar_inscripcion(id_inscripcion)
        
        if not inscripcion_entity:
            return GenericResponse.create_error(
                message="Inscripción no encontrada",
                errors=[f"Inscripción con ID {id_inscripcion} no existe"],
                status=404
            )
        
        inscripcion_response = InscripcionResponse(
            id_inscripcion=inscripcion_entity.id_inscripcion,
            id_usuario=inscripcion_entity.id_usuario,
            id_ciclo=inscripcion_entity.id_ciclo,
            fecha_inscripcion=inscripcion_entity.fecha_inscripcion,
            estado=inscripcion_entity.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Inscripción finalizada exitosamente",
            data=inscripcion_response,
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
            message="Error al finalizar inscripción",
            errors=[str(e)],
            status=500
        )