# src/app/features/carrera/presentation/routers/carrera_router.py
from fastapi import APIRouter, Depends
from typing import Annotated, List
from src.app.features.carrera.application.services.carrera_service import CarreraService
from src.app.features.carrera.application.dtos import CreateCarreraDTO, UpdateCarreraDTO
from src.app.features.carrera.infrastructure.dependencies import carrera_service_dep
from src.app.features.carrera.presentation.schemas.carrera_schemas import (
    CarreraCreateRequest,
    CarreraUpdateRequest,
    CarreraResponse,
    CarrerasListResponse,
    CarreraSingleResponse,
    CarreraDeleteResponse
)
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/carreras", tags=["carreras"])

@router.get("/", response_model=CarrerasListResponse)
def get_all_carreras(service: carrera_service_dep):
    try:
        carreras = service.get_all()
        
        carreras_response = [
            CarreraResponse(
                id_carrera=carrera.id_carrera,
                carrera=carrera.carrera.valor,
                facultad=carrera.facultad.valor
            ) for carrera in carreras
        ]
        
        return GenericResponse.create_success(
            message="Carreras obtenidas exitosamente",
            data=carreras_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener carreras",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_carrera}", response_model=CarreraSingleResponse)
def get_carrera_by_id(id_carrera: int, service: carrera_service_dep):
    try:
        carrera = service.get_by_id(id_carrera)
        if not carrera:
            return GenericResponse.create_error(
                message="Carrera no encontrada",
                errors=[f"Carrera con ID {id_carrera} no existe"],
                status=404
            )
        
        carrera_response = CarreraResponse(
            id_carrera=carrera.id_carrera,
            carrera=carrera.carrera.valor,
            facultad=carrera.facultad.valor
        )
        
        return GenericResponse.create_success(
            message="Carrera obtenida exitosamente",
            data=carrera_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener carrera",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=CarreraSingleResponse, status_code=201)
def create_carrera(carrera_request: CarreraCreateRequest, service: carrera_service_dep):
    try:
        create_dto = CreateCarreraDTO(
            carrera=carrera_request.carrera,
            facultad=carrera_request.facultad
        )
        
        carrera_entity = service.create(create_dto)
        
        carrera_response = CarreraResponse(
            id_carrera=carrera_entity.id_carrera,
            carrera=carrera_entity.carrera.valor,
            facultad=carrera_entity.facultad.valor
        )
        
        return GenericResponse.create_success(
            message="Carrera creada exitosamente",
            data=carrera_response,
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
            message="Error al crear carrera",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_carrera}", response_model=CarreraSingleResponse)
def update_carrera(id_carrera: int, carrera_request: CarreraUpdateRequest, service: carrera_service_dep):
    try:
        update_dto = UpdateCarreraDTO(
            carrera=carrera_request.carrera,
            facultad=carrera_request.facultad
        )
        
        carrera_entity = service.update(id_carrera, update_dto)
        
        if not carrera_entity:
            return GenericResponse.create_error(
                message="Carrera no encontrada",
                errors=[f"Carrera con ID {id_carrera} no existe"],
                status=404
            )
        
        carrera_response = CarreraResponse(
            id_carrera=carrera_entity.id_carrera,
            carrera=carrera_entity.carrera.valor,
            facultad=carrera_entity.facultad.valor
        )
        
        return GenericResponse.create_success(
            message="Carrera actualizada exitosamente",
            data=carrera_response,
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
            message="Error al actualizar carrera",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_carrera}", response_model=CarreraDeleteResponse)
def delete_carrera(id_carrera: int, service: carrera_service_dep):
    try:
        success = service.delete(id_carrera)
        
        if not success:
            return GenericResponse.create_error(
                message="Carrera no encontrada",
                errors=[f"Carrera con ID {id_carrera} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Carrera eliminada exitosamente",
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
            message="Error al eliminar carrera",
            errors=[str(e)],
            status=500
        )

@router.get("/nombre/{nombre_carrera}", response_model=CarreraSingleResponse)
def get_carrera_by_nombre(nombre_carrera: str, service: carrera_service_dep):
    try:
        carrera = service.get_by_nombre(nombre_carrera)
        if not carrera:
            return GenericResponse.create_error(
                message="Carrera no encontrada",
                errors=[f"Carrera con nombre '{nombre_carrera}' no existe"],
                status=404
            )
        
        carrera_response = CarreraResponse(
            id_carrera=carrera.id_carrera,
            carrera=carrera.carrera.valor,
            facultad=carrera.facultad.valor
        )
        
        return GenericResponse.create_success(
            message="Carrera obtenida exitosamente",
            data=carrera_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener carrera",
            errors=[str(e)],
            status=500
        )