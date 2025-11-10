# src/app/features/administrativo/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.administrativo.infrastructure.repositories.administrativo_repository_impl import AdministrativoRepositoryImpl
from src.app.features.administrativo.application.services.administrativo_service import AdministrativoService

# Importar dependencias de User
from src.app.features.user.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

def get_administrativo_repository(session: session_dep) -> AdministrativoRepositoryImpl:
    return AdministrativoRepositoryImpl(session=session)

def get_user_repository(session: session_dep) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=session)

def get_administrativo_service(
    administrativo_repository: Annotated[AdministrativoRepositoryImpl, Depends(get_administrativo_repository)],
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)]
) -> AdministrativoService:
    return AdministrativoService(
        administrativo_repository=administrativo_repository,
        user_repository=user_repository
    )

administrativo_service_dep = Annotated[AdministrativoService, Depends(get_administrativo_service)]