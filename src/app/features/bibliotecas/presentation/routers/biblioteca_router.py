# src/app/features/bibliotecas/presentation/routers/biblioteca_router.py
from fastapi import APIRouter, Depends
from typing import Annotated, List
from src.app.features.bibliotecas.application.services.biblioteca_service import BibliotecaService
from src.app.features.bibliotecas.application.dtos import CreateBibliotecaDTO, UpdateBibliotecaDTO
from src.app.features.bibliotecas.infrastructure.dependencies import biblioteca_service_dep
from src.app.features.bibliotecas.presentation.schemas.biblioteca_schemas import (
    BibliotecaCreateRequest,
    BibliotecaUpdateRequest,
    BibliotecaResponse,
    BibliotecasListResponse,
    BibliotecaSingleResponse,
    BibliotecaDeleteResponse
)
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/bibliotecas", tags=["bibliotecas"])

@router.get("/", response_model=BibliotecasListResponse)
def get_all_bibliotecas(service: biblioteca_service_dep):
    try:
        bibliotecas = service.get_all()
        
        bibliotecas_response = [
            BibliotecaResponse(
                id_biblioteca=bib.id_biblioteca,
                nombre=bib.nombre,
                ubicacion=bib.ubicacion
            ) for bib in bibliotecas
        ]
        
        return GenericResponse.create_success(
            message="Bibliotecas obtenidas exitosamente",
            data=bibliotecas_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener bibliotecas",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_biblioteca}", response_model=BibliotecaSingleResponse)
def get_biblioteca_by_id(id_biblioteca: int, service: biblioteca_service_dep):
    try:
        biblioteca = service.get_by_id(id_biblioteca)
        if not biblioteca:
            return GenericResponse.create_error(
                message="Biblioteca no encontrada",
                errors=[f"Biblioteca con ID {id_biblioteca} no existe"],
                status=404
            )
        
        biblioteca_response = BibliotecaResponse(
            id_biblioteca=biblioteca.id_biblioteca,
            nombre=biblioteca.nombre,
            ubicacion=biblioteca.ubicacion
        )
        
        return GenericResponse.create_success(
            message="Biblioteca obtenida exitosamente",
            data=biblioteca_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener biblioteca",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=BibliotecaSingleResponse, status_code=201)
def create_biblioteca(biblioteca_request: BibliotecaCreateRequest, service: biblioteca_service_dep):
    try:
        create_dto = CreateBibliotecaDTO(
            nombre=biblioteca_request.nombre,
            ubicacion=biblioteca_request.ubicacion
        )
        
        biblioteca_entity = service.create(create_dto)
        
        biblioteca_response = BibliotecaResponse(
            id_biblioteca=biblioteca_entity.id_biblioteca,
            nombre=biblioteca_entity.nombre,
            ubicacion=biblioteca_entity.ubicacion
        )
        
        return GenericResponse.create_success(
            message="Biblioteca creada exitosamente",
            data=biblioteca_response,
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
            message="Error al crear biblioteca",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_biblioteca}", response_model=BibliotecaSingleResponse)
def update_biblioteca(id_biblioteca: int, biblioteca_request: BibliotecaUpdateRequest, service: biblioteca_service_dep):
    try:
        update_dto = UpdateBibliotecaDTO(
            nombre=biblioteca_request.nombre,
            ubicacion=biblioteca_request.ubicacion
        )
        
        biblioteca_entity = service.update(id_biblioteca, update_dto)
        
        if not biblioteca_entity:
            return GenericResponse.create_error(
                message="Biblioteca no encontrada",
                errors=[f"Biblioteca con ID {id_biblioteca} no existe"],
                status=404
            )
        
        biblioteca_response = BibliotecaResponse(
            id_biblioteca=biblioteca_entity.id_biblioteca,
            nombre=biblioteca_entity.nombre,
            ubicacion=biblioteca_entity.ubicacion
        )
        
        return GenericResponse.create_success(
            message="Biblioteca actualizada exitosamente",
            data=biblioteca_response,
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
            message="Error al actualizar biblioteca",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_biblioteca}", response_model=BibliotecaDeleteResponse)
def delete_biblioteca(id_biblioteca: int, service: biblioteca_service_dep):
    try:
        success = service.delete(id_biblioteca)
        
        if not success:
            return GenericResponse.create_error(
                message="Biblioteca no encontrada",
                errors=[f"Biblioteca con ID {id_biblioteca} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Biblioteca eliminada exitosamente",
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
            message="Error al eliminar biblioteca",
            errors=[str(e)],
            status=500
        )

@router.get("/nombre/{nombre}", response_model=BibliotecaSingleResponse)
def get_biblioteca_by_nombre(nombre: str, service: biblioteca_service_dep):
    try:
        biblioteca = service.get_by_nombre(nombre)
        if not biblioteca:
            return GenericResponse.create_error(
                message="Biblioteca no encontrada",
                errors=[f"Biblioteca con nombre {nombre} no existe"],
                status=404
            )
        
        biblioteca_response = BibliotecaResponse(
            id_biblioteca=biblioteca.id_biblioteca,
            nombre=biblioteca.nombre,
            ubicacion=biblioteca.ubicacion
        )
        
        return GenericResponse.create_success(
            message="Biblioteca obtenida exitosamente",
            data=biblioteca_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener biblioteca",
            errors=[str(e)],
            status=500
        )