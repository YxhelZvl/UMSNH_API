# src/app/features/prestamos/presentation/routers/prestamo_router.py
from fastapi import APIRouter, Depends
from typing import Annotated, List
from datetime import date, datetime, timedelta
from src.app.features.prestamos.application.services.prestamo_service import PrestamoService
from src.app.features.prestamos.application.dtos import CreatePrestamoDTO, UpdatePrestamoDTO, DevolverPrestamoDTO, RenovarPrestamoDTO
from src.app.features.prestamos.infrastructure.dependencies import prestamo_service_dep
from src.app.features.prestamos.presentation.schemas.prestamo_schemas import (
    PrestamoCreateRequest,
    PrestamoUpdateRequest,
    PrestamoDevolverRequest,
    PrestamoRenovarRequest,
    PrestamoResponse,
    PrestamosListResponse,
    PrestamoSingleResponse,
    PrestamoDeleteResponse,
    PrestamoDetailResponse,
    PrestamoDetailSingleResponse,
    PrestamosDetailListResponse,
    UsuarioBasicResponse,
    EjemplarBasicResponse,
    CatalogoBasicResponse
)
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/prestamos", tags=["prestamos"])

# Endpoints básicos (solo datos de préstamo)
@router.get("/", response_model=PrestamosListResponse)
def get_all_prestamos(service: prestamo_service_dep):
    try:
        prestamos = service.get_all()
        
        prestamos_response = [
            PrestamoResponse(
                id_prestamo=prestamo.id_prestamo,
                id_usuario=prestamo.id_usuario,
                id_ejemplar=prestamo.id_ejemplar,
                fecha_prestamo=prestamo.fechas.fecha_prestamo,
                fecha_devolucion_esperada=prestamo.fechas.fecha_devolucion_esperada,
                fecha_devolucion_real=prestamo.fechas.fecha_devolucion_real,
                estado=prestamo.estado.valor.value
            ) for prestamo in prestamos
        ]
        
        return GenericResponse.create_success(
            message="Préstamos obtenidos exitosamente",
            data=prestamos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener préstamos",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_prestamo}", response_model=PrestamoSingleResponse)
def get_prestamo_by_id(id_prestamo: int, service: prestamo_service_dep):
    try:
        prestamo = service.get_by_id(id_prestamo)
        if not prestamo:
            return GenericResponse.create_error(
                message="Préstamo no encontrado",
                errors=[f"Préstamo con ID {id_prestamo} no existe"],
                status=404
            )
        
        prestamo_response = PrestamoResponse(
            id_prestamo=prestamo.id_prestamo,
            id_usuario=prestamo.id_usuario,
            id_ejemplar=prestamo.id_ejemplar,
            fecha_prestamo=prestamo.fechas.fecha_prestamo,
            fecha_devolucion_esperada=prestamo.fechas.fecha_devolucion_esperada,
            fecha_devolucion_real=prestamo.fechas.fecha_devolucion_real,
            estado=prestamo.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Préstamo obtenido exitosamente",
            data=prestamo_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener préstamo",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=PrestamoSingleResponse, status_code=201)
def create_prestamo(prestamo_request: PrestamoCreateRequest, service: prestamo_service_dep):
    try:
        create_dto = CreatePrestamoDTO(
            id_usuario=prestamo_request.id_usuario,
            id_ejemplar=prestamo_request.id_ejemplar,
            fecha_devolucion_esperada=prestamo_request.fecha_devolucion_esperada,
            estado=prestamo_request.estado
        )
        
        prestamo_entity = service.create(create_dto)
        
        prestamo_response = PrestamoResponse(
            id_prestamo=prestamo_entity.id_prestamo,
            id_usuario=prestamo_entity.id_usuario,
            id_ejemplar=prestamo_entity.id_ejemplar,
            fecha_prestamo=prestamo_entity.fechas.fecha_prestamo,
            fecha_devolucion_esperada=prestamo_entity.fechas.fecha_devolucion_esperada,
            fecha_devolucion_real=prestamo_entity.fechas.fecha_devolucion_real,
            estado=prestamo_entity.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Préstamo creado exitosamente",
            data=prestamo_response,
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
            message="Error al crear préstamo",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_prestamo}", response_model=PrestamoSingleResponse)
def update_prestamo(id_prestamo: int, prestamo_request: PrestamoUpdateRequest, service: prestamo_service_dep):
    try:
        update_dto = UpdatePrestamoDTO(
            id_usuario=prestamo_request.id_usuario,
            id_ejemplar=prestamo_request.id_ejemplar,
            fecha_devolucion_esperada=prestamo_request.fecha_devolucion_esperada,
            estado=prestamo_request.estado
        )
        
        prestamo_entity = service.update(id_prestamo, update_dto)
        
        if not prestamo_entity:
            return GenericResponse.create_error(
                message="Préstamo no encontrado",
                errors=[f"Préstamo con ID {id_prestamo} no existe"],
                status=404
            )
        
        prestamo_response = PrestamoResponse(
            id_prestamo=prestamo_entity.id_prestamo,
            id_usuario=prestamo_entity.id_usuario,
            id_ejemplar=prestamo_entity.id_ejemplar,
            fecha_prestamo=prestamo_entity.fechas.fecha_prestamo,
            fecha_devolucion_esperada=prestamo_entity.fechas.fecha_devolucion_esperada,
            fecha_devolucion_real=prestamo_entity.fechas.fecha_devolucion_real,
            estado=prestamo_entity.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Préstamo actualizado exitosamente",
            data=prestamo_response,
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
            message="Error al actualizar préstamo",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_prestamo}", response_model=PrestamoDeleteResponse)
def delete_prestamo(id_prestamo: int, service: prestamo_service_dep):
    try:
        success = service.delete(id_prestamo)
        
        if not success:
            return GenericResponse.create_error(
                message="Préstamo no encontrado",
                errors=[f"Préstamo con ID {id_prestamo} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Préstamo eliminado exitosamente",
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
            message="Error al eliminar préstamo",
            errors=[str(e)],
            status=500
        )

# Endpoints de búsqueda
@router.get("/usuario/{id_usuario}", response_model=PrestamosListResponse)
def get_prestamos_by_usuario(id_usuario: int, service: prestamo_service_dep):
    try:
        prestamos = service.get_by_usuario(id_usuario)
        
        prestamos_response = [
            PrestamoResponse(
                id_prestamo=prestamo.id_prestamo,
                id_usuario=prestamo.id_usuario,
                id_ejemplar=prestamo.id_ejemplar,
                fecha_prestamo=prestamo.fechas.fecha_prestamo,
                fecha_devolucion_esperada=prestamo.fechas.fecha_devolucion_esperada,
                fecha_devolucion_real=prestamo.fechas.fecha_devolucion_real,
                estado=prestamo.estado.valor.value
            ) for prestamo in prestamos
        ]
        
        return GenericResponse.create_success(
            message="Préstamos obtenidos exitosamente por usuario",
            data=prestamos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener préstamos por usuario",
            errors=[str(e)],
            status=500
        )

@router.get("/ejemplar/{id_ejemplar}", response_model=PrestamosListResponse)
def get_prestamos_by_ejemplar(id_ejemplar: int, service: prestamo_service_dep):
    try:
        prestamos = service.get_by_ejemplar(id_ejemplar)
        
        prestamos_response = [
            PrestamoResponse(
                id_prestamo=prestamo.id_prestamo,
                id_usuario=prestamo.id_usuario,
                id_ejemplar=prestamo.id_ejemplar,
                fecha_prestamo=prestamo.fechas.fecha_prestamo,
                fecha_devolucion_esperada=prestamo.fechas.fecha_devolucion_esperada,
                fecha_devolucion_real=prestamo.fechas.fecha_devolucion_real,
                estado=prestamo.estado.valor.value
            ) for prestamo in prestamos
        ]
        
        return GenericResponse.create_success(
            message="Préstamos obtenidos exitosamente por ejemplar",
            data=prestamos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener préstamos por ejemplar",
            errors=[str(e)],
            status=500
        )

@router.get("/estado/{estado}", response_model=PrestamosListResponse)
def get_prestamos_by_estado(estado: str, service: prestamo_service_dep):
    try:
        prestamos = service.get_by_estado(estado)
        
        prestamos_response = [
            PrestamoResponse(
                id_prestamo=prestamo.id_prestamo,
                id_usuario=prestamo.id_usuario,
                id_ejemplar=prestamo.id_ejemplar,
                fecha_prestamo=prestamo.fechas.fecha_prestamo,
                fecha_devolucion_esperada=prestamo.fechas.fecha_devolucion_esperada,
                fecha_devolucion_real=prestamo.fechas.fecha_devolucion_real,
                estado=prestamo.estado.valor.value
            ) for prestamo in prestamos
        ]
        
        return GenericResponse.create_success(
            message="Préstamos obtenidos exitosamente por estado",
            data=prestamos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener préstamos por estado",
            errors=[str(e)],
            status=500
        )

# Endpoints específicos
@router.get("/estado/activos", response_model=PrestamosListResponse)
def get_prestamos_activos(service: prestamo_service_dep):
    try:
        prestamos = service.get_prestamos_activos()
        
        prestamos_response = [
            PrestamoResponse(
                id_prestamo=prestamo.id_prestamo,
                id_usuario=prestamo.id_usuario,
                id_ejemplar=prestamo.id_ejemplar,
                fecha_prestamo=prestamo.fechas.fecha_prestamo,
                fecha_devolucion_esperada=prestamo.fechas.fecha_devolucion_esperada,
                fecha_devolucion_real=prestamo.fechas.fecha_devolucion_real,
                estado=prestamo.estado.valor.value
            ) for prestamo in prestamos
        ]
        
        return GenericResponse.create_success(
            message="Préstamos activos obtenidos exitosamente",
            data=prestamos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener préstamos activos",
            errors=[str(e)],
            status=500
        )

@router.get("/estado/retrasados", response_model=PrestamosListResponse)
def get_prestamos_retrasados(service: prestamo_service_dep):
    try:
        prestamos = service.get_prestamos_retrasados()
        
        prestamos_response = [
            PrestamoResponse(
                id_prestamo=prestamo.id_prestamo,
                id_usuario=prestamo.id_usuario,
                id_ejemplar=prestamo.id_ejemplar,
                fecha_prestamo=prestamo.fechas.fecha_prestamo,
                fecha_devolucion_esperada=prestamo.fechas.fecha_devolucion_esperada,
                fecha_devolucion_real=prestamo.fechas.fecha_devolucion_real,
                estado=prestamo.estado.valor.value
            ) for prestamo in prestamos
        ]
        
        return GenericResponse.create_success(
            message="Préstamos retrasados obtenidos exitosamente",
            data=prestamos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener préstamos retrasados",
            errors=[str(e)],
            status=500
        )

@router.get("/por-vencer/{dias}", response_model=PrestamosListResponse)
def get_prestamos_por_vencer(dias: int, service: prestamo_service_dep):
    try:
        prestamos = service.get_prestamos_por_vencer(dias)
        
        prestamos_response = [
            PrestamoResponse(
                id_prestamo=prestamo.id_prestamo,
                id_usuario=prestamo.id_usuario,
                id_ejemplar=prestamo.id_ejemplar,
                fecha_prestamo=prestamo.fechas.fecha_prestamo,
                fecha_devolucion_esperada=prestamo.fechas.fecha_devolucion_esperada,
                fecha_devolucion_real=prestamo.fechas.fecha_devolucion_real,
                estado=prestamo.estado.valor.value
            ) for prestamo in prestamos
        ]
        
        return GenericResponse.create_success(
            message=f"Préstamos por vencer en {dias} días obtenidos exitosamente",
            data=prestamos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener préstamos por vencer",
            errors=[str(e)],
            status=500
        )

# Endpoints detallados (con información de usuario, ejemplar y catálogo)
@router.get("/detalles/", response_model=PrestamosDetailListResponse)
def get_all_prestamos_detalles(service: prestamo_service_dep):
    try:
        prestamos_detallados = service.get_all_with_details()
        
        prestamos_response = []
        for detalle in prestamos_detallados:
            prestamo_db = detalle['prestamo']
            user_db = detalle['usuario']
            ejemplar_db = detalle['ejemplar']
            catalogo_db = detalle['catalogo']
            
            # Calcular días de retraso
            dias_retraso = 0
            if prestamo_db.estado == "activo" and prestamo_db.fecha_devolucion_esperada < date.today():
                dias_retraso = (date.today() - prestamo_db.fecha_devolucion_esperada).days
            
            prestamo_detail = PrestamoDetailResponse(
                id_prestamo=prestamo_db.id_prestamo,
                usuario=UsuarioBasicResponse(
                    id_usuario=user_db.id_usuario,
                    nombre=user_db.nombre,
                    apellidoP=user_db.apellidoP,
                    apellidoM=user_db.apellidoM,
                    matricula=user_db.matricula,
                    email=user_db.email
                ),
                ejemplar=EjemplarBasicResponse(
                    id_ejemplar=ejemplar_db.id_ejemplar,
                    codigo_inventario=ejemplar_db.codigo_inventario,
                    ubicacion=ejemplar_db.ubicacion,
                    estado=ejemplar_db.estado
                ),
                catalogo=CatalogoBasicResponse(
                    id_catalogo=catalogo_db.id_catalogo,
                    tipo=catalogo_db.tipo,
                    nombre=catalogo_db.nombre,
                    autor=catalogo_db.autor,
                    isbn=catalogo_db.isbn
                ),
                fecha_prestamo=prestamo_db.fecha_prestamo,
                fecha_devolucion_esperada=prestamo_db.fecha_devolucion_esperada,
                fecha_devolucion_real=prestamo_db.fecha_devolucion_real,
                estado=prestamo_db.estado,
                dias_retraso=dias_retraso if dias_retraso > 0 else None
            )
            prestamos_response.append(prestamo_detail)
        
        return GenericResponse.create_success(
            message="Préstamos obtenidos exitosamente con detalles",
            data=prestamos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener préstamos con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_prestamo}/detalles", response_model=PrestamoDetailSingleResponse)
def get_prestamo_detalles_by_id(id_prestamo: int, service: prestamo_service_dep):
    try:
        prestamo_detallado = service.get_by_id_with_details(id_prestamo)
        if not prestamo_detallado:
            return GenericResponse.create_error(
                message="Préstamo no encontrado",
                errors=[f"Préstamo con ID {id_prestamo} no existe"],
                status=404
            )
        
        prestamo_db = prestamo_detallado['prestamo']
        user_db = prestamo_detallado['usuario']
        ejemplar_db = prestamo_detallado['ejemplar']
        catalogo_db = prestamo_detallado['catalogo']
        
        # Calcular días de retraso
        dias_retraso = 0
        if prestamo_db.estado == "activo" and prestamo_db.fecha_devolucion_esperada < date.today():
            dias_retraso = (date.today() - prestamo_db.fecha_devolucion_esperada).days
        
        prestamo_response = PrestamoDetailResponse(
            id_prestamo=prestamo_db.id_prestamo,
            usuario=UsuarioBasicResponse(
                id_usuario=user_db.id_usuario,
                nombre=user_db.nombre,
                apellidoP=user_db.apellidoP,
                apellidoM=user_db.apellidoM,
                matricula=user_db.matricula,
                email=user_db.email
            ),
            ejemplar=EjemplarBasicResponse(
                id_ejemplar=ejemplar_db.id_ejemplar,
                codigo_inventario=ejemplar_db.codigo_inventario,
                ubicacion=ejemplar_db.ubicacion,
                estado=ejemplar_db.estado
            ),
            catalogo=CatalogoBasicResponse(
                id_catalogo=catalogo_db.id_catalogo,
                tipo=catalogo_db.tipo,
                nombre=catalogo_db.nombre,
                autor=catalogo_db.autor,
                isbn=catalogo_db.isbn
            ),
            fecha_prestamo=prestamo_db.fecha_prestamo,
            fecha_devolucion_esperada=prestamo_db.fecha_devolucion_esperada,
            fecha_devolucion_real=prestamo_db.fecha_devolucion_real,
            estado=prestamo_db.estado,
            dias_retraso=dias_retraso if dias_retraso > 0 else None
        )
        
        return GenericResponse.create_success(
            message="Préstamo obtenido exitosamente con detalles",
            data=prestamo_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener préstamo con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/usuario/{id_usuario}/detalles", response_model=PrestamosDetailListResponse)
def get_prestamos_detalles_by_usuario(id_usuario: int, service: prestamo_service_dep):
    try:
        prestamos_detallados = service.get_by_usuario_with_details(id_usuario)
        
        prestamos_response = []
        for detalle in prestamos_detallados:
            prestamo_db = detalle['prestamo']
            user_db = detalle['usuario']
            ejemplar_db = detalle['ejemplar']
            catalogo_db = detalle['catalogo']
            
            # Calcular días de retraso
            dias_retraso = 0
            if prestamo_db.estado == "activo" and prestamo_db.fecha_devolucion_esperada < date.today():
                dias_retraso = (date.today() - prestamo_db.fecha_devolucion_esperada).days
            
            prestamo_detail = PrestamoDetailResponse(
                id_prestamo=prestamo_db.id_prestamo,
                usuario=UsuarioBasicResponse(
                    id_usuario=user_db.id_usuario,
                    nombre=user_db.nombre,
                    apellidoP=user_db.apellidoP,
                    apellidoM=user_db.apellidoM,
                    matricula=user_db.matricula,
                    email=user_db.email
                ),
                ejemplar=EjemplarBasicResponse(
                    id_ejemplar=ejemplar_db.id_ejemplar,
                    codigo_inventario=ejemplar_db.codigo_inventario,
                    ubicacion=ejemplar_db.ubicacion,
                    estado=ejemplar_db.estado
                ),
                catalogo=CatalogoBasicResponse(
                    id_catalogo=catalogo_db.id_catalogo,
                    tipo=catalogo_db.tipo,
                    nombre=catalogo_db.nombre,
                    autor=catalogo_db.autor,
                    isbn=catalogo_db.isbn
                ),
                fecha_prestamo=prestamo_db.fecha_prestamo,
                fecha_devolucion_esperada=prestamo_db.fecha_devolucion_esperada,
                fecha_devolucion_real=prestamo_db.fecha_devolucion_real,
                estado=prestamo_db.estado,
                dias_retraso=dias_retraso if dias_retraso > 0 else None
            )
            prestamos_response.append(prestamo_detail)
        
        return GenericResponse.create_success(
            message="Préstamos por usuario obtenidos exitosamente con detalles",
            data=prestamos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener préstamos por usuario con detalles",
            errors=[str(e)],
            status=500
        )

# Endpoints de acciones de negocio
@router.post("/{id_prestamo}/devolver", response_model=PrestamoSingleResponse)
def devolver_prestamo(id_prestamo: int, devolver_request: PrestamoDevolverRequest, service: prestamo_service_dep):
    try:
        devolver_dto = DevolverPrestamoDTO(
            fecha_devolucion_real=devolver_request.fecha_devolucion_real
        )
        
        prestamo_entity = service.devolver(id_prestamo, devolver_dto)
        
        if not prestamo_entity:
            return GenericResponse.create_error(
                message="Préstamo no encontrado",
                errors=[f"Préstamo con ID {id_prestamo} no existe"],
                status=404
            )
        
        prestamo_response = PrestamoResponse(
            id_prestamo=prestamo_entity.id_prestamo,
            id_usuario=prestamo_entity.id_usuario,
            id_ejemplar=prestamo_entity.id_ejemplar,
            fecha_prestamo=prestamo_entity.fechas.fecha_prestamo,
            fecha_devolucion_esperada=prestamo_entity.fechas.fecha_devolucion_esperada,
            fecha_devolucion_real=prestamo_entity.fechas.fecha_devolucion_real,
            estado=prestamo_entity.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Préstamo devuelto exitosamente",
            data=prestamo_response,
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
            message="Error al devolver préstamo",
            errors=[str(e)],
            status=500
        )

@router.post("/{id_prestamo}/renovar", response_model=PrestamoSingleResponse)
def renovar_prestamo(id_prestamo: int, renovar_request: PrestamoRenovarRequest, service: prestamo_service_dep):
    try:
        renovar_dto = RenovarPrestamoDTO(
            nueva_fecha_devolucion=renovar_request.nueva_fecha_devolucion
        )
        
        prestamo_entity = service.renovar(id_prestamo, renovar_dto)
        
        if not prestamo_entity:
            return GenericResponse.create_error(
                message="Préstamo no encontrado",
                errors=[f"Préstamo con ID {id_prestamo} no existe"],
                status=404
            )
        
        prestamo_response = PrestamoResponse(
            id_prestamo=prestamo_entity.id_prestamo,
            id_usuario=prestamo_entity.id_usuario,
            id_ejemplar=prestamo_entity.id_ejemplar,
            fecha_prestamo=prestamo_entity.fechas.fecha_prestamo,
            fecha_devolucion_esperada=prestamo_entity.fechas.fecha_devolucion_esperada,
            fecha_devolucion_real=prestamo_entity.fechas.fecha_devolucion_real,
            estado=prestamo_entity.estado.valor.value
        )
        
        return GenericResponse.create_success(
            message="Préstamo renovado exitosamente",
            data=prestamo_response,
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
            message="Error al renovar préstamo",
            errors=[str(e)],
            status=500
        )

@router.post("/marcar-retrasados", response_model=GenericResponse[dict])
def marcar_prestamos_retrasados(service: prestamo_service_dep):
    try:
        service.marcar_retrasados()
        
        prestamos_retrasados = service.get_prestamos_retrasados()
        
        return GenericResponse.create_success(
            message="Préstamos retrasados marcados exitosamente",
            data={"prestamos_retrasados": len(prestamos_retrasados)},
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al marcar préstamos retrasados",
            errors=[str(e)],
            status=500
        )