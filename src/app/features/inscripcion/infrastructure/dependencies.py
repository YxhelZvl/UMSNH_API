# src/app/features/inscripcion/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.inscripcion.infrastructure.repositories.inscripcion_repository_impl import InscripcionRepositoryImpl
from src.app.features.inscripcion.application.services.inscripcion_service import InscripcionService

# Importar dependencias de User y Ciclo
from src.app.features.user.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.app.features.ciclo.infrastructure.repositories.ciclo_repository_impl import CicloRepositoryImpl

def get_inscripcion_repository(session: session_dep) -> InscripcionRepositoryImpl:
    return InscripcionRepositoryImpl(session=session)

def get_user_repository(session: session_dep) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=session)

def get_ciclo_repository(session: session_dep) -> CicloRepositoryImpl:
    return CicloRepositoryImpl(session=session)

def get_inscripcion_service(
    inscripcion_repository: Annotated[InscripcionRepositoryImpl, Depends(get_inscripcion_repository)],
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)],
    ciclo_repository: Annotated[CicloRepositoryImpl, Depends(get_ciclo_repository)]
) -> InscripcionService:
    return InscripcionService(
        inscripcion_repository=inscripcion_repository,
        user_repository=user_repository,
        ciclo_repository=ciclo_repository
    )

inscripcion_service_dep = Annotated[InscripcionService, Depends(get_inscripcion_service)]