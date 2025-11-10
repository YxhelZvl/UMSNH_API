# src/app/features/carrera/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.carrera.infrastructure.repositories.carrera_repository_impl import CarreraRepositoryImpl
from src.app.features.carrera.application.services.carrera_service import CarreraService

def get_carrera_repository(session: session_dep) -> CarreraRepositoryImpl:
    return CarreraRepositoryImpl(session=session)

def get_carrera_service(carrera_repository: Annotated[CarreraRepositoryImpl, Depends(get_carrera_repository)]) -> CarreraService:
    return CarreraService(carrera_repository=carrera_repository)

carrera_repository_dep = Annotated[CarreraRepositoryImpl, Depends(get_carrera_repository)]
carrera_service_dep = Annotated[CarreraService, Depends(get_carrera_service)]