# src/app/features/ciclo/presentation/routers/ciclo_router.py
from fastapi import APIRouter, Depends
from typing import Annotated, List
from datetime import date
from src.app.features.ciclo.application.services.ciclo_service import CicloService
from src.app.features.ciclo.application.dtos import CreateCicloDTO, UpdateCicloDTO
from src.app.features.ciclo.infrastructure.dependencies import ciclo_service_dep
from src.app.features.ciclo.presentation.schemas.ciclo_schemas import (
    CicloCreateRequest,
    CicloUpdateRequest,
    CicloResponse,
    CiclosListResponse,
    CicloSingleResponse,
    CicloDeleteResponse,
    LastIdCycleResponse,
    LastSingleIdCycleResponse
)
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/ciclos", tags=["ciclos"])

@router.get("/", response_model=CiclosListResponse)
def get_all_ciclos(service: ciclo_service_dep):
    try:
        ciclos = service.get_all()
        
        ciclos_response = [
            CicloResponse(
                id_ciclo=ciclo.id_ciclo,
                ciclo=ciclo.ciclo.valor,
                fecha_inicio=ciclo.rango_fechas.fecha_inicio,
                fecha_final=ciclo.rango_fechas.fecha_final
            ) for ciclo in ciclos
        ]
        
        return GenericResponse.create_success(
            message="Ciclos obtenidos exitosamente",
            data=ciclos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ciclos",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_ciclo}", response_model=CicloSingleResponse)
def get_ciclo_by_id(id_ciclo: int, service: ciclo_service_dep):
    try:
        ciclo = service.get_by_id(id_ciclo)
        if not ciclo:
            return GenericResponse.create_error(
                message="Ciclo no encontrado",
                errors=[f"Ciclo con ID {id_ciclo} no existe"],
                status=404
            )
        
        ciclo_response = CicloResponse(
            id_ciclo=ciclo.id_ciclo,
            ciclo=ciclo.ciclo.valor,
            fecha_inicio=ciclo.rango_fechas.fecha_inicio,
            fecha_final=ciclo.rango_fechas.fecha_final
        )
        
        return GenericResponse.create_success(
            message="Ciclo obtenido exitosamente",
            data=ciclo_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ciclo",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=CicloSingleResponse, status_code=201)
def create_ciclo(ciclo_request: CicloCreateRequest, service: ciclo_service_dep):
    try:
        create_dto = CreateCicloDTO(
            ciclo=ciclo_request.ciclo,
            fecha_inicio=ciclo_request.fecha_inicio,
            fecha_final=ciclo_request.fecha_final
        )
        
        ciclo_entity = service.create(create_dto)
        
        ciclo_response = CicloResponse(
            id_ciclo=ciclo_entity.id_ciclo,
            ciclo=ciclo_entity.ciclo.valor,
            fecha_inicio=ciclo_entity.rango_fechas.fecha_inicio,
            fecha_final=ciclo_entity.rango_fechas.fecha_final,
        )
        
        return GenericResponse.create_success(
            message="Ciclo creado exitosamente",
            data=ciclo_response,
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
            message="Error al crear ciclo",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_ciclo}", response_model=CicloSingleResponse)
def update_ciclo(id_ciclo: int, ciclo_request: CicloUpdateRequest, service: ciclo_service_dep):
    try:
        update_dto = UpdateCicloDTO(
            ciclo=ciclo_request.ciclo,
            fecha_inicio=ciclo_request.fecha_inicio,
            fecha_final=ciclo_request.fecha_final
        )
        
        ciclo_entity = service.update(id_ciclo, update_dto)
        
        if not ciclo_entity:
            return GenericResponse.create_error(
                message="Ciclo no encontrado",
                errors=[f"Ciclo con ID {id_ciclo} no existe"],
                status=404
            )
        
        ciclo_response = CicloResponse(
            id_ciclo=ciclo_entity.id_ciclo,
            ciclo=ciclo_entity.ciclo.valor,
            fecha_inicio=ciclo_entity.rango_fechas.fecha_inicio,
            fecha_final=ciclo_entity.rango_fechas.fecha_final,
        )
        
        return GenericResponse.create_success(
            message="Ciclo actualizado exitosamente",
            data=ciclo_response,
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
            message="Error al actualizar ciclo",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_ciclo}", response_model=CicloDeleteResponse)
def delete_ciclo(id_ciclo: int, service: ciclo_service_dep):
    try:
        success = service.delete(id_ciclo)
        
        if not success:
            return GenericResponse.create_error(
                message="Ciclo no encontrado",
                errors=[f"Ciclo con ID {id_ciclo} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Ciclo eliminado exitosamente",
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
            message="Error al eliminar ciclo",
            errors=[str(e)],
            status=500
        )

@router.get("/nombre/{nombre_ciclo}", response_model=CicloSingleResponse)
def get_ciclo_by_nombre(nombre_ciclo: str, service: ciclo_service_dep):
    try:
        ciclo = service.get_by_nombre(nombre_ciclo)
        if not ciclo:
            return GenericResponse.create_error(
                message="Ciclo no encontrado",
                errors=[f"Ciclo con nombre '{nombre_ciclo}' no existe"],
                status=404
            )
        
        ciclo_response = CicloResponse(
            id_ciclo=ciclo.id_ciclo,
            ciclo=ciclo.ciclo.valor,
            fecha_inicio=ciclo.rango_fechas.fecha_inicio,
            fecha_final=ciclo.rango_fechas.fecha_final,
        )
        
        return GenericResponse.create_success(
            message="Ciclo obtenido exitosamente",
            data=ciclo_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ciclo",
            errors=[str(e)],
            status=500
        )

@router.get("/estado/activos", response_model=CiclosListResponse)
def get_ciclos_activos(service: ciclo_service_dep):
    try:
        ciclos = service.get_ciclos_activos()
        
        ciclos_response = [
            CicloResponse(
                id_ciclo=ciclo.id_ciclo,
                ciclo=ciclo.ciclo.valor,
                fecha_inicio=ciclo.rango_fechas.fecha_inicio,
                fecha_final=ciclo.rango_fechas.fecha_final,
            ) for ciclo in ciclos
        ]
        
        return GenericResponse.create_success(
            message="Ciclos activos obtenidos exitosamente",
            data=ciclos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ciclos activos",
            errors=[str(e)],
            status=500
        )

@router.get("/fecha/{fecha}", response_model=CiclosListResponse)
def get_ciclos_por_fecha(fecha: date, service: ciclo_service_dep):
    try:
        ciclos = service.get_ciclos_por_fecha(fecha)
        
        ciclos_response = [
            CicloResponse(
                id_ciclo=ciclo.id_ciclo,
                ciclo=ciclo.ciclo.valor,
                fecha_inicio=ciclo.rango_fechas.fecha_inicio,
                fecha_final=ciclo.rango_fechas.fecha_final,
            ) for ciclo in ciclos
        ]
        
        return GenericResponse.create_success(
            message=f"Ciclos para la fecha {fecha} obtenidos exitosamente",
            data=ciclos_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener ciclos por fecha",
            errors=[str(e)],
            status=500
        )
@router.get("/last-id/", response_model=LastSingleIdCycleResponse)
def get_last_cycle_id(service: ciclo_service_dep):
    try:
        last_id = service.get_last_cycle_id()
        print("Last ID obtenido:", last_id)
        if last_id is None:
            return GenericResponse.create_error(
                message="No hay ciclos disponibles",
                errors=["No se encontró ningún ciclo"],
                status=404
            )
        last_id_response = LastIdCycleResponse(
            last_id_cycle=last_id
        )
        return GenericResponse.create_success(
            message="Último ID de ciclo obtenido exitosamente",
            data=last_id_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener el último ID de ciclo",
            errors=[str(e)],
            status=500
        )
        