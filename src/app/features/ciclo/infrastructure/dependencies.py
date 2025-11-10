# src/app/features/ciclo/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.ciclo.infrastructure.repositories.ciclo_repository_impl import CicloRepositoryImpl
from src.app.features.ciclo.application.services.ciclo_service import CicloService

def get_ciclo_repository(session: session_dep) -> CicloRepositoryImpl:
    return CicloRepositoryImpl(session=session)

def get_ciclo_service(ciclo_repository: Annotated[CicloRepositoryImpl, Depends(get_ciclo_repository)]) -> CicloService:
    return CicloService(ciclo_repository=ciclo_repository)

ciclo_repository_dep = Annotated[CicloRepositoryImpl, Depends(get_ciclo_repository)]
ciclo_service_dep = Annotated[CicloService, Depends(get_ciclo_service)]