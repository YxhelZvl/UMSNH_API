# src/app/features/catalogo/presentation/routers/catalogo_router.py
from fastapi import APIRouter, Depends
from typing import Annotated, List
from src.app.features.catalogo.application.services.catalogo_service import CatalogoService
from src.app.features.catalogo.application.dtos import CreateCatalogoDTO, UpdateCatalogoDTO
from src.app.features.catalogo.infrastructure.dependencies import catalogo_service_dep
from src.app.features.catalogo.presentation.schemas.catalogo_schemas import (
    CatalogoCreateRequest,
    CatalogoUpdateRequest,
    CatalogoResponse,
    CatalogosListResponse,
    CatalogoSingleResponse,
    CatalogoDeleteResponse
)
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/catalogo", tags=["catalogo"])

@router.get("/", response_model=CatalogosListResponse)
def get_all_catalogo(service: catalogo_service_dep):
    try:
        catalogos = service.get_all()
        
        catalogos_response = [
            CatalogoResponse(
                id_catalogo=cat.id_catalogo,
                tipo=cat.tipo.valor.value,
                nombre=cat.nombre.valor,
                autor=cat.autor,
                isbn=cat.isbn.valor if cat.isbn else None,
                descripcion=cat.descripcion
            ) for cat in catalogos
        ]
        
        return GenericResponse.create_success(
            message="Items del catálogo obtenidos exitosamente",
            data=catalogos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener items del catálogo",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_catalogo}", response_model=CatalogoSingleResponse)
def get_catalogo_by_id(id_catalogo: int, service: catalogo_service_dep):
    try:
        catalogo = service.get_by_id(id_catalogo)
        if not catalogo:
            return GenericResponse.create_error(
                message="Item del catálogo no encontrado",
                errors=[f"Item del catálogo con ID {id_catalogo} no existe"],
                status=404
            )
        
        catalogo_response = CatalogoResponse(
            id_catalogo=catalogo.id_catalogo,
            tipo=catalogo.tipo.valor.value,
            nombre=catalogo.nombre.valor,
            autor=catalogo.autor,
            isbn=catalogo.isbn.valor if catalogo.isbn else None,
            descripcion=catalogo.descripcion
        )
        
        return GenericResponse.create_success(
            message="Item del catálogo obtenido exitosamente",
            data=catalogo_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener item del catálogo",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=CatalogoSingleResponse, status_code=201)
def create_catalogo(catalogo_request: CatalogoCreateRequest, service: catalogo_service_dep):
    try:
        create_dto = CreateCatalogoDTO(
            tipo=catalogo_request.tipo,
            nombre=catalogo_request.nombre,
            autor=catalogo_request.autor,
            isbn=catalogo_request.isbn,
            descripcion=catalogo_request.descripcion
        )
        
        catalogo_entity = service.create(create_dto)
        
        catalogo_response = CatalogoResponse(
            id_catalogo=catalogo_entity.id_catalogo,
            tipo=catalogo_entity.tipo.valor.value,
            nombre=catalogo_entity.nombre.valor,
            autor=catalogo_entity.autor,
            isbn=catalogo_entity.isbn.valor if catalogo_entity.isbn else None,
            descripcion=catalogo_entity.descripcion
        )
        
        return GenericResponse.create_success(
            message="Item del catálogo creado exitosamente",
            data=catalogo_response,
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
            message="Error al crear item del catálogo",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_catalogo}", response_model=CatalogoSingleResponse)
def update_catalogo(id_catalogo: int, catalogo_request: CatalogoUpdateRequest, service: catalogo_service_dep):
    try:
        update_dto = UpdateCatalogoDTO(
            tipo=catalogo_request.tipo,
            nombre=catalogo_request.nombre,
            autor=catalogo_request.autor,
            isbn=catalogo_request.isbn,
            descripcion=catalogo_request.descripcion
        )
        
        catalogo_entity = service.update(id_catalogo, update_dto)
        
        if not catalogo_entity:
            return GenericResponse.create_error(
                message="Item del catálogo no encontrado",
                errors=[f"Item del catálogo con ID {id_catalogo} no existe"],
                status=404
            )
        
        catalogo_response = CatalogoResponse(
            id_catalogo=catalogo_entity.id_catalogo,
            tipo=catalogo_entity.tipo.valor.value,
            nombre=catalogo_entity.nombre.valor,
            autor=catalogo_entity.autor,
            isbn=catalogo_entity.isbn.valor if catalogo_entity.isbn else None,
            descripcion=catalogo_entity.descripcion
        )
        
        return GenericResponse.create_success(
            message="Item del catálogo actualizado exitosamente",
            data=catalogo_response,
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
            message="Error al actualizar item del catálogo",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_catalogo}", response_model=CatalogoDeleteResponse)
def delete_catalogo(id_catalogo: int, service: catalogo_service_dep):
    try:
        success = service.delete(id_catalogo)
        
        if not success:
            return GenericResponse.create_error(
                message="Item del catálogo no encontrado",
                errors=[f"Item del catálogo con ID {id_catalogo} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Item del catálogo eliminado exitosamente",
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
            message="Error al eliminar item del catálogo",
            errors=[str(e)],
            status=500
        )

@router.get("/nombre/{nombre}", response_model=CatalogoSingleResponse)
def get_catalogo_by_nombre(nombre: str, service: catalogo_service_dep):
    try:
        catalogo = service.get_by_nombre(nombre)
        if not catalogo:
            return GenericResponse.create_error(
                message="Item del catálogo no encontrado",
                errors=[f"Item del catálogo con nombre {nombre} no existe"],
                status=404
            )
        
        catalogo_response = CatalogoResponse(
            id_catalogo=catalogo.id_catalogo,
            tipo=catalogo.tipo.valor.value,
            nombre=catalogo.nombre.valor,
            autor=catalogo.autor,
            isbn=catalogo.isbn.valor if catalogo.isbn else None,
            descripcion=catalogo.descripcion
        )
        
        return GenericResponse.create_success(
            message="Item del catálogo obtenido exitosamente",
            data=catalogo_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener item del catálogo",
            errors=[str(e)],
            status=500
        )

@router.get("/tipo/{tipo}", response_model=CatalogosListResponse)
def get_catalogo_by_tipo(tipo: str, service: catalogo_service_dep):
    try:
        catalogos = service.get_by_tipo(tipo)
        
        catalogos_response = [
            CatalogoResponse(
                id_catalogo=cat.id_catalogo,
                tipo=cat.tipo.valor.value,
                nombre=cat.nombre.valor,
                autor=cat.autor,
                isbn=cat.isbn.valor if cat.isbn else None,
                descripcion=cat.descripcion
            ) for cat in catalogos
        ]
        
        return GenericResponse.create_success(
            message="Items del catálogo obtenidos exitosamente por tipo",
            data=catalogos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener items del catálogo por tipo",
            errors=[str(e)],
            status=500
        )

@router.get("/autor/{autor}", response_model=CatalogosListResponse)
def get_catalogo_by_autor(autor: str, service: catalogo_service_dep):
    try:
        catalogos = service.get_by_autor(autor)
        
        catalogos_response = [
            CatalogoResponse(
                id_catalogo=cat.id_catalogo,
                tipo=cat.tipo.valor.value,
                nombre=cat.nombre.valor,
                autor=cat.autor,
                isbn=cat.isbn.valor if cat.isbn else None,
                descripcion=cat.descripcion
            ) for cat in catalogos
        ]
        
        return GenericResponse.create_success(
            message="Items del catálogo obtenidos exitosamente por autor",
            data=catalogos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener items del catálogo por autor",
            errors=[str(e)],
            status=500
        )

@router.get("/isbn/{isbn}", response_model=CatalogoSingleResponse)
def get_catalogo_by_isbn(isbn: str, service: catalogo_service_dep):
    try:
        catalogo = service.get_by_isbn(isbn)
        if not catalogo:
            return GenericResponse.create_error(
                message="Item del catálogo no encontrado",
                errors=[f"Item del catálogo con ISBN {isbn} no existe"],
                status=404
            )
        
        catalogo_response = CatalogoResponse(
            id_catalogo=catalogo.id_catalogo,
            tipo=catalogo.tipo.valor.value,
            nombre=catalogo.nombre.valor,
            autor=catalogo.autor,
            isbn=catalogo.isbn.valor if catalogo.isbn else None,
            descripcion=catalogo.descripcion
        )
        
        return GenericResponse.create_success(
            message="Item del catálogo obtenido exitosamente por ISBN",
            data=catalogo_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener item del catálogo por ISBN",
            errors=[str(e)],
            status=500
        )

# Endpoints para tipos específicos
@router.get("/tipo/libro", response_model=CatalogosListResponse)
def get_libros(service: catalogo_service_dep):
    try:
        libros = service.get_libros()
        
        libros_response = [
            CatalogoResponse(
                id_catalogo=libro.id_catalogo,
                tipo=libro.tipo.valor.value,
                nombre=libro.nombre.valor,
                autor=libro.autor,
                isbn=libro.isbn.valor if libro.isbn else None,
                descripcion=libro.descripcion
            ) for libro in libros
        ]
        
        return GenericResponse.create_success(
            message="Libros obtenidos exitosamente",
            data=libros_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener libros",
            errors=[str(e)],
            status=500
        )

@router.get("/tipo/herramienta", response_model=CatalogosListResponse)
def get_herramientas(service: catalogo_service_dep):
    try:
        herramientas = service.get_herramientas()
        
        herramientas_response = [
            CatalogoResponse(
                id_catalogo=herramienta.id_catalogo,
                tipo=herramienta.tipo.valor.value,
                nombre=herramienta.nombre.valor,
                autor=herramienta.autor,
                isbn=herramienta.isbn.valor if herramienta.isbn else None,
                descripcion=herramienta.descripcion
            ) for herramienta in herramientas
        ]
        
        return GenericResponse.create_success(
            message="Herramientas obtenidas exitosamente",
            data=herramientas_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener herramientas",
            errors=[str(e)],
            status=500
        )

@router.get("/tipo/equipo", response_model=CatalogosListResponse)
def get_equipos(service: catalogo_service_dep):
    try:
        equipos = service.get_equipos()
        
        equipos_response = [
            CatalogoResponse(
                id_catalogo=equipo.id_catalogo,
                tipo=equipo.tipo.valor.value,
                nombre=equipo.nombre.valor,
                autor=equipo.autor,
                isbn=equipo.isbn.valor if equipo.isbn else None,
                descripcion=equipo.descripcion
            ) for equipo in equipos
        ]
        
        return GenericResponse.create_success(
            message="Equipos obtenidos exitosamente",
            data=equipos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener equipos",
            errors=[str(e)],
            status=500
        )