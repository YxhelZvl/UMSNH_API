# src/app/features/laboratorios/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.laboratorios.infrastructure.repositories.laboratorio_repository_impl import LaboratorioRepositoryImpl
from src.app.features.laboratorios.application.services.laboratorio_service import LaboratorioService

# Importar dependencias de User
from src.app.features.user.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

def get_laboratorio_repository(session: session_dep) -> LaboratorioRepositoryImpl:
    return LaboratorioRepositoryImpl(session=session)

def get_user_repository(session: session_dep) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=session)

def get_laboratorio_service(
    laboratorio_repository: Annotated[LaboratorioRepositoryImpl, Depends(get_laboratorio_repository)],
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)]
) -> LaboratorioService:
    return LaboratorioService(
        laboratorio_repository=laboratorio_repository,
        user_repository=user_repository
    )

laboratorio_service_dep = Annotated[LaboratorioService, Depends(get_laboratorio_service)]