# src/app/features/ejemplares/presentation/routers/ejemplar_router.py
from fastapi import APIRouter, Depends
from typing import Annotated, List
from src.app.features.ejemplares.application.services.ejemplar_service import EjemplarService
from src.app.features.ejemplares.application.dtos import CreateEjemplarDTO, UpdateEjemplarDTO
from src.app.features.ejemplares.infrastructure.dependencies import ejemplar_service_dep
from src.app.features.ejemplares.presentation.schemas.ejemplar_schemas import (
    EjemplarCreateRequest,
    EjemplarUpdateRequest,
    EjemplarResponse,
    EjemplaresListResponse,
    EjemplarSingleResponse,
    EjemplarDeleteResponse,
    EjemplarDetailResponse,
    EjemplarDetailSingleResponse,
    EjemplaresDetailListResponse,
    EjemplaresDisponiblesListResponse,
    CatalogoBasicResponse,
    BibliotecaBasicResponse,
    LaboratorioBasicResponse
)
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/ejemplares", tags=["ejemplares"])

# Endpoints básicos (solo datos de ejemplar)
@router.get("/", response_model=EjemplaresListResponse)
def get_all_ejemplares(service: ejemplar_service_dep):
    try:
        ejemplares = service.get_all()
        
        ejemplares_response = [
            EjemplarResponse(
                id_ejemplar=ejemplar.id_ejemplar,
                id_catalogo=ejemplar.id_catalogo,
                codigo_inventario=ejemplar.codigo_inventario.valor,
                ubicacion=ejemplar.ubicacion.valor.value,
                id_laboratorio=ejemplar.id_laboratorio,
                id_biblioteca=ejemplar.id_biblioteca,
                estado=ejemplar.estado.valor.value
            ) for ejemplar in ejemplares
        ]
        
        return GenericResponse.create_success(
            message="Ejemplares obtenidos exitosamente",
            data=ejemplares_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ejemplares",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_ejemplar}", response_model=EjemplarSingleResponse)
def get_ejemplar_by_id(id_ejemplar: int, service: ejemplar_service_dep):
    try:
        ejemplar = service.get_by_id(id_ejemplar)
        if not ejemplar:
            return GenericResponse.create_error(
                message="Ejemplar no encontrado",
                errors=[f"Ejemplar con ID {id_ejemplar} no existe"],
                status=404
            )
        
        ejemplar_response = EjemplarResponse(
            id_ejemplar=ejemplar.id_ejemplar,
            id_catalogo=ejemplar.id_catalogo,
            codigo_inventario=ejemplar.codigo_inventario.valor,
            ubicacion=ejemplar.ubicacion.valor.value,
            id_laboratorio=ejemplar.id_laboratorio,
            id_biblioteca=ejemplar.id_biblioteca,
            estado=ejemplar.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Ejemplar obtenido exitosamente",
            data=ejemplar_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ejemplar",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=EjemplarSingleResponse, status_code=201)
def create_ejemplar(ejemplar_request: EjemplarCreateRequest, service: ejemplar_service_dep):
    try:
        create_dto = CreateEjemplarDTO(
            id_catalogo=ejemplar_request.id_catalogo,
            codigo_inventario=ejemplar_request.codigo_inventario,
            ubicacion=ejemplar_request.ubicacion,
            id_laboratorio=ejemplar_request.id_laboratorio,
            id_biblioteca=ejemplar_request.id_biblioteca,
            estado=ejemplar_request.estado
        )
        
        ejemplar_entity = service.create(create_dto)
        
        ejemplar_response = EjemplarResponse(
            id_ejemplar=ejemplar_entity.id_ejemplar,
            id_catalogo=ejemplar_entity.id_catalogo,
            codigo_inventario=ejemplar_entity.codigo_inventario.valor,
            ubicacion=ejemplar_entity.ubicacion.valor.value,
            id_laboratorio=ejemplar_entity.id_laboratorio,
            id_biblioteca=ejemplar_entity.id_biblioteca,
            estado=ejemplar_entity.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Ejemplar creado exitosamente",
            data=ejemplar_response,
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
            message="Error al crear ejemplar",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_ejemplar}", response_model=EjemplarSingleResponse)
def update_ejemplar(id_ejemplar: int, ejemplar_request: EjemplarUpdateRequest, service: ejemplar_service_dep):
    try:
        update_dto = UpdateEjemplarDTO(
            id_catalogo=ejemplar_request.id_catalogo,
            codigo_inventario=ejemplar_request.codigo_inventario,
            ubicacion=ejemplar_request.ubicacion,
            id_laboratorio=ejemplar_request.id_laboratorio,
            id_biblioteca=ejemplar_request.id_biblioteca,
            estado=ejemplar_request.estado
        )
        
        ejemplar_entity = service.update(id_ejemplar, update_dto)
        
        if not ejemplar_entity:
            return GenericResponse.create_error(
                message="Ejemplar no encontrado",
                errors=[f"Ejemplar con ID {id_ejemplar} no existe"],
                status=404
            )
        
        ejemplar_response = EjemplarResponse(
            id_ejemplar=ejemplar_entity.id_ejemplar,
            id_catalogo=ejemplar_entity.id_catalogo,
            codigo_inventario=ejemplar_entity.codigo_inventario.valor,
            ubicacion=ejemplar_entity.ubicacion.valor.value,
            id_laboratorio=ejemplar_entity.id_laboratorio,
            id_biblioteca=ejemplar_entity.id_biblioteca,
            estado=ejemplar_entity.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Ejemplar actualizado exitosamente",
            data=ejemplar_response,
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
            message="Error al actualizar ejemplar",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_ejemplar}", response_model=EjemplarDeleteResponse)
def delete_ejemplar(id_ejemplar: int, service: ejemplar_service_dep):
    try:
        success = service.delete(id_ejemplar)
        
        if not success:
            return GenericResponse.create_error(
                message="Ejemplar no encontrado",
                errors=[f"Ejemplar con ID {id_ejemplar} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Ejemplar eliminado exitosamente",
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
            message="Error al eliminar ejemplar",
            errors=[str(e)],
            status=500
        )

# Endpoints de búsqueda
@router.get("/codigo/{codigo_inventario}", response_model=EjemplarSingleResponse)
def get_ejemplar_by_codigo_inventario(codigo_inventario: str, service: ejemplar_service_dep):
    try:
        ejemplar = service.get_by_codigo_inventario(codigo_inventario)
        if not ejemplar:
            return GenericResponse.create_error(
                message="Ejemplar no encontrado",
                errors=[f"Ejemplar con código de inventario {codigo_inventario} no existe"],
                status=404
            )
        
        ejemplar_response = EjemplarResponse(
            id_ejemplar=ejemplar.id_ejemplar,
            id_catalogo=ejemplar.id_catalogo,
            codigo_inventario=ejemplar.codigo_inventario.valor,
            ubicacion=ejemplar.ubicacion.valor.value,
            id_laboratorio=ejemplar.id_laboratorio,
            id_biblioteca=ejemplar.id_biblioteca,
            estado=ejemplar.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Ejemplar obtenido exitosamente",
            data=ejemplar_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ejemplar",
            errors=[str(e)],
            status=500
        )

@router.get("/catalogo/{id_catalogo}", response_model=EjemplaresListResponse)
def get_ejemplares_by_catalogo(id_catalogo: int, service: ejemplar_service_dep):
    try:
        ejemplares = service.get_by_catalogo(id_catalogo)
        
        ejemplares_response = [
            EjemplarResponse(
                id_ejemplar=ejemplar.id_ejemplar,
                id_catalogo=ejemplar.id_catalogo,
                codigo_inventario=ejemplar.codigo_inventario.valor,
                ubicacion=ejemplar.ubicacion.valor.value,
                id_laboratorio=ejemplar.id_laboratorio,
                id_biblioteca=ejemplar.id_biblioteca,
                estado=ejemplar.estado.valor.value
            ) for ejemplar in ejemplares
        ]
        
        return GenericResponse.create_success(
            message="Ejemplares obtenidos exitosamente por catálogo",
            data=ejemplares_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ejemplares por catálogo",
            errors=[str(e)],
            status=500
        )

@router.get("/ubicacion/{ubicacion}", response_model=EjemplaresListResponse)
def get_ejemplares_by_ubicacion(ubicacion: str, service: ejemplar_service_dep):
    try:
        ejemplares = service.get_by_ubicacion(ubicacion)
        
        ejemplares_response = [
            EjemplarResponse(
                id_ejemplar=ejemplar.id_ejemplar,
                id_catalogo=ejemplar.id_catalogo,
                codigo_inventario=ejemplar.codigo_inventario.valor,
                ubicacion=ejemplar.ubicacion.valor.value,
                id_laboratorio=ejemplar.id_laboratorio,
                id_biblioteca=ejemplar.id_biblioteca,
                estado=ejemplar.estado.valor.value
            ) for ejemplar in ejemplares
        ]
        
        return GenericResponse.create_success(
            message="Ejemplares obtenidos exitosamente por ubicación",
            data=ejemplares_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ejemplares por ubicación",
            errors=[str(e)],
            status=500
        )

@router.get("/estado/{estado}", response_model=EjemplaresListResponse)
def get_ejemplares_by_estado(estado: str, service: ejemplar_service_dep):
    try:
        ejemplares = service.get_by_estado(estado)
        
        ejemplares_response = [
            EjemplarResponse(
                id_ejemplar=ejemplar.id_ejemplar,
                id_catalogo=ejemplar.id_catalogo,
                codigo_inventario=ejemplar.codigo_inventario.valor,
                ubicacion=ejemplar.ubicacion.valor.value,
                id_laboratorio=ejemplar.id_laboratorio,
                id_biblioteca=ejemplar.id_biblioteca,
                estado=ejemplar.estado.valor.value
            ) for ejemplar in ejemplares
        ]
        
        return GenericResponse.create_success(
            message="Ejemplares obtenidos exitosamente por estado",
            data=ejemplares_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ejemplares por estado",
            errors=[str(e)],
            status=500
        )

@router.get("/biblioteca/{id_biblioteca}", response_model=EjemplaresListResponse)
def get_ejemplares_by_biblioteca(id_biblioteca: int, service: ejemplar_service_dep):
    try:
        ejemplares = service.get_by_biblioteca(id_biblioteca)
        
        ejemplares_response = [
            EjemplarResponse(
                id_ejemplar=ejemplar.id_ejemplar,
                id_catalogo=ejemplar.id_catalogo,
                codigo_inventario=ejemplar.codigo_inventario.valor,
                ubicacion=ejemplar.ubicacion.valor.value,
                id_laboratorio=ejemplar.id_laboratorio,
                id_biblioteca=ejemplar.id_biblioteca,
                estado=ejemplar.estado.valor.value
            ) for ejemplar in ejemplares
        ]
        
        return GenericResponse.create_success(
            message="Ejemplares obtenidos exitosamente por biblioteca",
            data=ejemplares_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ejemplares por biblioteca",
            errors=[str(e)],
            status=500
        )

@router.get("/laboratorio/{id_laboratorio}", response_model=EjemplaresListResponse)
def get_ejemplares_by_laboratorio(id_laboratorio: int, service: ejemplar_service_dep):
    try:
        ejemplares = service.get_by_laboratorio(id_laboratorio)
        
        ejemplares_response = [
            EjemplarResponse(
                id_ejemplar=ejemplar.id_ejemplar,
                id_catalogo=ejemplar.id_catalogo,
                codigo_inventario=ejemplar.codigo_inventario.valor,
                ubicacion=ejemplar.ubicacion.valor.value,
                id_laboratorio=ejemplar.id_laboratorio,
                id_biblioteca=ejemplar.id_biblioteca,
                estado=ejemplar.estado.valor.value
            ) for ejemplar in ejemplares
        ]
        
        return GenericResponse.create_success(
            message="Ejemplares obtenidos exitosamente por laboratorio",
            data=ejemplares_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ejemplares por laboratorio",
            errors=[str(e)],
            status=500
        )

# Endpoints detallados (con información de catálogo, biblioteca, laboratorio)
@router.get("/detalles/", response_model=EjemplaresDetailListResponse)
def get_all_ejemplares_detalles(service: ejemplar_service_dep):
    try:
        ejemplares_detallados = service.get_all_with_details()
        
        ejemplares_response = []
        for detalle in ejemplares_detallados:
            ejemplar_db = detalle['ejemplar']
            catalogo_db = detalle['catalogo']
            biblioteca_db = detalle['biblioteca']
            laboratorio_db = detalle['laboratorio']
            
            ejemplar_detail = EjemplarDetailResponse(
                id_ejemplar=ejemplar_db.id_ejemplar,
                catalogo=CatalogoBasicResponse(
                    id_catalogo=catalogo_db.id_catalogo,
                    tipo=catalogo_db.tipo,
                    nombre=catalogo_db.nombre,
                    autor=catalogo_db.autor,
                    isbn=catalogo_db.isbn,
                    descripcion=catalogo_db.descripcion
                ),
                codigo_inventario=ejemplar_db.codigo_inventario,
                ubicacion=ejemplar_db.ubicacion,
                biblioteca=BibliotecaBasicResponse(
                    id_biblioteca=biblioteca_db.id_biblioteca,
                    nombre=biblioteca_db.nombre,
                    ubicacion=biblioteca_db.ubicacion
                ) if biblioteca_db else None,
                laboratorio=LaboratorioBasicResponse(
                    id_laboratorio=laboratorio_db.id_laboratorio,
                    nombre=laboratorio_db.nombre,
                    ubicacion=laboratorio_db.ubicacion,
                    responsable_id=laboratorio_db.responsable_id
                ) if laboratorio_db else None,
                estado=ejemplar_db.estado
            )
            ejemplares_response.append(ejemplar_detail)
        
        return GenericResponse.create_success(
            message="Ejemplares obtenidos exitosamente con detalles",
            data=ejemplares_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ejemplares con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_ejemplar}/detalles", response_model=EjemplarDetailSingleResponse)
def get_ejemplar_detalles_by_id(id_ejemplar: int, service: ejemplar_service_dep):
    try:
        ejemplar_detallado = service.get_by_id_with_details(id_ejemplar)
        if not ejemplar_detallado:
            return GenericResponse.create_error(
                message="Ejemplar no encontrado",
                errors=[f"Ejemplar con ID {id_ejemplar} no existe"],
                status=404
            )
        
        ejemplar_db = ejemplar_detallado['ejemplar']
        catalogo_db = ejemplar_detallado['catalogo']
        biblioteca_db = ejemplar_detallado['biblioteca']
        laboratorio_db = ejemplar_detallado['laboratorio']
        
        ejemplar_response = EjemplarDetailResponse(
            id_ejemplar=ejemplar_db.id_ejemplar,
            catalogo=CatalogoBasicResponse(
                id_catalogo=catalogo_db.id_catalogo,
                tipo=catalogo_db.tipo,
                nombre=catalogo_db.nombre,
                autor=catalogo_db.autor,
                isbn=catalogo_db.isbn,
                descripcion=catalogo_db.descripcion
            ),
            codigo_inventario=ejemplar_db.codigo_inventario,
            ubicacion=ejemplar_db.ubicacion,
            biblioteca=BibliotecaBasicResponse(
                id_biblioteca=biblioteca_db.id_biblioteca,
                nombre=biblioteca_db.nombre,
                ubicacion=biblioteca_db.ubicacion
            ) if biblioteca_db else None,
            laboratorio=LaboratorioBasicResponse(
                id_laboratorio=laboratorio_db.id_laboratorio,
                nombre=laboratorio_db.nombre,
                ubicacion=laboratorio_db.ubicacion,
                responsable_id=laboratorio_db.responsable_id
            ) if laboratorio_db else None,
            estado=ejemplar_db.estado
        )
        
        return GenericResponse.create_success(
            message="Ejemplar obtenido exitosamente con detalles",
            data=ejemplar_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ejemplar con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/disponibles/prestamo", response_model=EjemplaresDisponiblesListResponse)
def get_ejemplares_disponibles_for_prestamo(service: ejemplar_service_dep):
    try:
        ejemplares_disponibles = service.get_disponibles_for_prestamo()
        
        ejemplares_response = []
        for detalle in ejemplares_disponibles:
            ejemplar_db = detalle['ejemplar']
            catalogo_db = detalle['catalogo']
            
            ejemplar_detail = EjemplarDetailResponse(
                id_ejemplar=ejemplar_db.id_ejemplar,
                catalogo=CatalogoBasicResponse(
                    id_catalogo=catalogo_db.id_catalogo,
                    tipo=catalogo_db.tipo,
                    nombre=catalogo_db.nombre,
                    autor=catalogo_db.autor,
                    isbn=catalogo_db.isbn,
                    descripcion=catalogo_db.descripcion
                ),
                codigo_inventario=ejemplar_db.codigo_inventario,
                ubicacion=ejemplar_db.ubicacion,
                biblioteca=None,  # No incluimos estos detalles para simplificar
                laboratorio=None,
                estado=ejemplar_db.estado
            )
            ejemplares_response.append(ejemplar_detail)
        
        return GenericResponse.create_success(
            message="Ejemplares disponibles para préstamo obtenidos exitosamente",
            data=ejemplares_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ejemplares disponibles para préstamo",
            errors=[str(e)],
            status=500
        )

# Endpoints de acciones de negocio
@router.post("/{id_ejemplar}/prestar", response_model=EjemplarSingleResponse)
def prestar_ejemplar(id_ejemplar: int, service: ejemplar_service_dep):
    try:
        ejemplar = service.marcar_como_prestado(id_ejemplar)
        
        if not ejemplar:
            return GenericResponse.create_error(
                message="Ejemplar no encontrado",
                errors=[f"Ejemplar con ID {id_ejemplar} no existe"],
                status=404
            )
        
        ejemplar_response = EjemplarResponse(
            id_ejemplar=ejemplar.id_ejemplar,
            id_catalogo=ejemplar.id_catalogo,
            codigo_inventario=ejemplar.codigo_inventario.valor,
            ubicacion=ejemplar.ubicacion.valor.value,
            id_laboratorio=ejemplar.id_laboratorio,
            id_biblioteca=ejemplar.id_biblioteca,
            estado=ejemplar.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Ejemplar marcado como prestado exitosamente",
            data=ejemplar_response,
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
            message="Error al prestar ejemplar",
            errors=[str(e)],
            status=500
        )

@router.post("/{id_ejemplar}/devolver", response_model=EjemplarSingleResponse)
def devolver_ejemplar(id_ejemplar: int, service: ejemplar_service_dep):
    try:
        ejemplar = service.marcar_como_devuelto(id_ejemplar)
        
        if not ejemplar:
            return GenericResponse.create_error(
                message="Ejemplar no encontrado",
                errors=[f"Ejemplar con ID {id_ejemplar} no existe"],
                status=404
            )
        
        ejemplar_response = EjemplarResponse(
            id_ejemplar=ejemplar.id_ejemplar,
            id_catalogo=ejemplar.id_catalogo,
            codigo_inventario=ejemplar.codigo_inventario.valor,
            ubicacion=ejemplar.ubicacion.valor.value,
            id_laboratorio=ejemplar.id_laboratorio,
            id_biblioteca=ejemplar.id_biblioteca,
            estado=ejemplar.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Ejemplar marcado como devuelto exitosamente",
            data=ejemplar_response,
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
            message="Error al devolver ejemplar",
            errors=[str(e)],
            status=500
        )