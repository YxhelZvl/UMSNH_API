# src/app/features/estudiante/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.estudiante.infrastructure.repositories.estudiante_repository_impl import EstudianteRepositoryImpl
from src.app.features.estudiante.application.services.estudiante_service import EstudianteService

# Importar dependencias de User y Carrera
from src.app.features.user.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.app.features.carrera.infrastructure.repositories.carrera_repository_impl import CarreraRepositoryImpl

def get_estudiante_repository(session: session_dep) -> EstudianteRepositoryImpl:
    return EstudianteRepositoryImpl(session=session)

def get_user_repository(session: session_dep) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=session)

def get_carrera_repository(session: session_dep) -> CarreraRepositoryImpl:
    return CarreraRepositoryImpl(session=session)

def get_estudiante_service(
    estudiante_repository: Annotated[EstudianteRepositoryImpl, Depends(get_estudiante_repository)],
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)],
    carrera_repository: Annotated[CarreraRepositoryImpl, Depends(get_carrera_repository)]
) -> EstudianteService:
    return EstudianteService(
        estudiante_repository=estudiante_repository,
        user_repository=user_repository,
        carrera_repository=carrera_repository
    )

estudiante_service_dep = Annotated[EstudianteService, Depends(get_estudiante_service)]