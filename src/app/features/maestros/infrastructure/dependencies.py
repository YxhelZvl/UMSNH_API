# src/app/features/maestros/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.maestros.infrastructure.repositories.maestro_repository_impl import MaestroRepositoryImpl
from src.app.features.maestros.application.services.maestro_service import MaestroService

# Importar dependencias de User
from src.app.features.user.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

def get_maestro_repository(session: session_dep) -> MaestroRepositoryImpl:
    return MaestroRepositoryImpl(session=session)

def get_user_repository(session: session_dep) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=session)

def get_maestro_service(
    maestro_repository: Annotated[MaestroRepositoryImpl, Depends(get_maestro_repository)],
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)]
) -> MaestroService:
    return MaestroService(
        maestro_repository=maestro_repository,
        user_repository=user_repository
    )

maestro_service_dep = Annotated[MaestroService, Depends(get_maestro_service)]