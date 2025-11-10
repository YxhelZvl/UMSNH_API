# src/app/features/estudiante/presentation/routers/estudiante_router.py
from fastapi import APIRouter, Depends
from typing import Annotated, List
from src.app.features.estudiante.application.services.estudiante_service import EstudianteService
from src.app.features.estudiante.application.dtos import CreateEstudianteDTO, UpdateEstudianteDTO
from src.app.features.estudiante.infrastructure.dependencies import estudiante_service_dep
from src.app.features.estudiante.presentation.schemas.estudiante_schemas import (
    EstudianteCreateRequest,
    EstudianteUpdateRequest,
    EstudianteResponse,
    EstudiantesListResponse,
    EstudianteSingleResponse,
    EstudianteDeleteResponse,
    EstudianteDetailResponse,
    EstudianteDetailSingleResponse,
    EstudiantesDetailListResponse,
    UsuarioBasicResponse,
    CarreraBasicResponse
)
from src.app.shared.schemas.generic_response import GenericResponse
from src.app.shared.schemas.generic_response import GenericResponse

router = APIRouter(prefix="/estudiantes", tags=["estudiantes"])

@router.get("/", response_model=EstudiantesListResponse)
def get_all_estudiantes(service: estudiante_service_dep):
    try:
        estudiantes = service.get_all()
        
        estudiantes_response = [
            EstudianteResponse(
                id_estudiante=estudiante.id_estudiante,
                id_usuario=estudiante.id_usuario,
                id_carrera=estudiante.id_carrera
            ) for estudiante in estudiantes
        ]
        
        return GenericResponse.create_success(
            message="Estudiantes obtenidos exitosamente",
            data=estudiantes_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener estudiantes",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_estudiante}", response_model=EstudianteSingleResponse)
def get_estudiante_by_id(id_estudiante: int, service: estudiante_service_dep):
    try:
        estudiante = service.get_by_id(id_estudiante)
        if not estudiante:
            return GenericResponse.create_error(
                message="Estudiante no encontrado",
                errors=[f"Estudiante con ID {id_estudiante} no existe"],
                status=404
            )
        
        estudiante_response = EstudianteResponse(
            id_estudiante=estudiante.id_estudiante,
            id_usuario=estudiante.id_usuario,
            id_carrera=estudiante.id_carrera
        )
        
        return GenericResponse.create_success(
            message="Estudiante obtenido exitosamente",
            data=estudiante_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener estudiante",
            errors=[str(e)],
            status=500
        )

@router.post("/", response_model=EstudianteSingleResponse, status_code=201)
def create_estudiante(estudiante_request: EstudianteCreateRequest, service: estudiante_service_dep):
    try:
        create_dto = CreateEstudianteDTO(
            id_usuario=estudiante_request.id_usuario,
            id_carrera=estudiante_request.id_carrera
        )
        
        estudiante_entity = service.create(create_dto)
        
        estudiante_response = EstudianteResponse(
            id_estudiante=estudiante_entity.id_estudiante,
            id_usuario=estudiante_entity.id_usuario,
            id_carrera=estudiante_entity.id_carrera
        )
        
        return GenericResponse.create_success(
            message="Estudiante creado exitosamente",
            data=estudiante_response,
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
            message="Error al crear estudiante",
            errors=[str(e)],
            status=500
        )

@router.put("/{id_estudiante}", response_model=EstudianteSingleResponse)
def update_estudiante(id_estudiante: int, estudiante_request: EstudianteUpdateRequest, service: estudiante_service_dep):
    try:
        update_dto = UpdateEstudianteDTO(
            id_carrera=estudiante_request.id_carrera
        )
        
        estudiante_entity = service.update(id_estudiante, update_dto)
        
        if not estudiante_entity:
            return GenericResponse.create_error(
                message="Estudiante no encontrado",
                errors=[f"Estudiante con ID {id_estudiante} no existe"],
                status=404
            )
        
        estudiante_response = EstudianteResponse(
            id_estudiante=estudiante_entity.id_estudiante,
            id_usuario=estudiante_entity.id_usuario,
            id_carrera=estudiante_entity.id_carrera
        )
        
        return GenericResponse.create_success(
            message="Estudiante actualizado exitosamente",
            data=estudiante_response,
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
            message="Error al actualizar estudiante",
            errors=[str(e)],
            status=500
        )

@router.delete("/{id_estudiante}", response_model=EstudianteDeleteResponse)
def delete_estudiante(id_estudiante: int, service: estudiante_service_dep):
    try:
        success = service.delete(id_estudiante)
        
        if not success:
            return GenericResponse.create_error(
                message="Estudiante no encontrado",
                errors=[f"Estudiante con ID {id_estudiante} no existe"],
                status=404
            )
        
        return GenericResponse.create_success(
            message="Estudiante eliminado exitosamente",
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
            message="Error al eliminar estudiante",
            errors=[str(e)],
            status=500
        )

@router.get("/usuario/{id_usuario}", response_model=EstudianteSingleResponse)
def get_estudiante_by_usuario_id(id_usuario: int, service: estudiante_service_dep):
    try:
        estudiante = service.get_by_usuario_id(id_usuario)
        if not estudiante:
            return GenericResponse.create_error(
                message="Estudiante no encontrado",
                errors=[f"Estudiante para el usuario con ID {id_usuario} no existe"],
                status=404
            )
        
        estudiante_response = EstudianteResponse(
            id_estudiante=estudiante.id_estudiante,
            id_usuario=estudiante.id_usuario,
            id_carrera=estudiante.id_carrera
        )
        
        return GenericResponse.create_success(
            message="Estudiante obtenido exitosamente",
            data=estudiante_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener estudiante",
            errors=[str(e)],
            status=500
        )

@router.get("/carrera/{id_carrera}", response_model=EstudiantesListResponse)
def get_estudiantes_by_carrera_id(id_carrera: int, service: estudiante_service_dep):
    try:
        estudiantes = service.get_by_carrera_id(id_carrera)
        
        estudiantes_response = [
            EstudianteResponse(
                id_estudiante=estudiante.id_estudiante,
                id_usuario=estudiante.id_usuario,
                id_carrera=estudiante.id_carrera
            ) for estudiante in estudiantes
        ]
        
        return GenericResponse.create_success(
            message="Estudiantes obtenidos exitosamente",
            data=estudiantes_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener estudiantes",
            errors=[str(e)],
            status=500
        )
        
@router.get("/detalles/", response_model=EstudiantesDetailListResponse)
def get_all_estudiantes_detalles(service: estudiante_service_dep):
    """Obtener todos los estudiantes con información detallada de usuario y carrera"""
    try:
        estudiantes_detallados = service.get_all_with_details()
        
        estudiantes_response = [
            EstudianteDetailResponse(
                id_estudiante=detalle['estudiante'].id_estudiante,
                usuario=UsuarioBasicResponse(
                    id_usuario=detalle['usuario'].id_usuario,
                    nombre=detalle['usuario'].nombre,  # Extraer string del Value Object
                    apellidoP=detalle['usuario'].apellidoP,
                    apellidoM=detalle['usuario'].apellidoM,
                    matricula=detalle['usuario'].matricula,  # Extraer string del Value Object
                    email=detalle['usuario'].email,  # Extraer string del Value Object
                    id_rol=detalle['usuario'].id_rol,
                    status=detalle['usuario'].status
                ),
                carrera=CarreraBasicResponse(
                    id_carrera=detalle['carrera'].id_carrera,
                    carrera=detalle['carrera'].carrera,  # Extraer string del Value Object
                    facultad=detalle['carrera'].facultad  # Extraer string del Value Object
                )
            ) for detalle in estudiantes_detallados
        ]
        
        return GenericResponse.create_success(
            message="Estudiantes obtenidos exitosamente con detalles",
            data=estudiantes_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener estudiantes con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/{id_estudiante}/detalles", response_model=EstudianteDetailSingleResponse)
def get_estudiante_detalles_by_id(id_estudiante: int, service: estudiante_service_dep):
    """Obtener un estudiante por ID con información detallada de usuario y carrera"""
    try:
        estudiante_detallado = service.get_by_id_with_details(id_estudiante)
        if not estudiante_detallado:
            return GenericResponse.create_error(
                message="Estudiante no encontrado",
                errors=[f"Estudiante con ID {id_estudiante} no existe"],
                status=404
            )
        
        estudiante_response = EstudianteDetailResponse(
            id_estudiante=estudiante_detallado['estudiante'].id_estudiante,
            usuario=UsuarioBasicResponse(
                id_usuario=estudiante_detallado['usuario'].id_usuario,
                nombre=estudiante_detallado['usuario'].nombre,
                apellidoP=estudiante_detallado['usuario'].apellidoP,
                apellidoM=estudiante_detallado['usuario'].apellidoM,
                matricula=estudiante_detallado['usuario'].matricula,
                email=estudiante_detallado['usuario'].email,
                id_rol=estudiante_detallado['usuario'].id_rol,
                status=estudiante_detallado['usuario'].status
            ),
            carrera=CarreraBasicResponse(
                id_carrera=estudiante_detallado['carrera'].id_carrera,
                carrera=estudiante_detallado['carrera'].carrera,
                facultad=estudiante_detallado['carrera'].facultad
            )
        )
        
        return GenericResponse.create_success(
            message="Estudiante obtenido exitosamente con detalles",
            data=estudiante_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener estudiante con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/usuario/{id_usuario}/detalles", response_model=EstudianteDetailSingleResponse)
def get_estudiante_detalles_by_usuario_id(id_usuario: int, service: estudiante_service_dep):
    """Obtener estudiante por ID de usuario con información detallada"""
    try:
        estudiante_detallado = service.get_by_usuario_id_with_details(id_usuario)
        if not estudiante_detallado:
            return GenericResponse.create_error(
                message="Estudiante no encontrado",
                errors=[f"Estudiante para el usuario con ID {id_usuario} no existe"],
                status=404
            )
        
        estudiante_response = EstudianteDetailResponse(
            id_estudiante=estudiante_detallado['estudiante'].id_estudiante,
            usuario=UsuarioBasicResponse(
                id_usuario=estudiante_detallado['usuario'].id_usuario,
                nombre=estudiante_detallado['usuario'].nombre,
                apellidoP=estudiante_detallado['usuario'].apellidoP,
                apellidoM=estudiante_detallado['usuario'].apellidoM,
                matricula=estudiante_detallado['usuario'].matricula,
                email=estudiante_detallado['usuario'].email,
                id_rol=estudiante_detallado['usuario'].id_rol,
                status=estudiante_detallado['usuario'].status
            ),
            carrera=CarreraBasicResponse(
                id_carrera=estudiante_detallado['carrera'].id_carrera,
                carrera=estudiante_detallado['carrera'].carrera,
                facultad=estudiante_detallado['carrera'].facultad
            )
        )
        
        return GenericResponse.create_success(
            message="Estudiante obtenido exitosamente con detalles",
            data=estudiante_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener estudiante con detalles",
            errors=[str(e)],
            status=500
        )

@router.get("/carrera/{id_carrera}/detalles", response_model=EstudiantesDetailListResponse)
def get_estudiantes_detalles_by_carrera_id(id_carrera: int, service: estudiante_service_dep):
    """Obtener estudiantes por ID de carrera con información detallada"""
    try:
        estudiantes_detallados = service.get_by_carrera_id_with_details(id_carrera)
        
        estudiantes_response = [
            EstudianteDetailResponse(
                id_estudiante=detalle['estudiante'].id_estudiante,
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
                carrera=CarreraBasicResponse(
                    id_carrera=detalle['carrera'].id_carrera,
                    carrera=detalle['carrera'].carrera,
                    facultad=detalle['carrera'].facultad
                )
            ) for detalle in estudiantes_detallados
        ]
        
        return GenericResponse.create_success(
            message="Estudiantes obtenidos exitosamente con detalles",
            data=estudiantes_response,
            status=200
        )
        
    except Exception as e:
        return GenericResponse.create_error(
            message="Error al obtener estudiantes con detalles",
            errors=[str(e)],
            status=500
        )