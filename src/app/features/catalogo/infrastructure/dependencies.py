# src/app/features/catalogo/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.catalogo.infrastructure.repositories.catalogo_repository_impl import CatalogoRepositoryImpl
from src.app.features.catalogo.application.services.catalogo_service import CatalogoService

def get_catalogo_repository(session: session_dep) -> CatalogoRepositoryImpl:
    return CatalogoRepositoryImpl(session=session)

def get_catalogo_service(
    catalogo_repository: Annotated[CatalogoRepositoryImpl, Depends(get_catalogo_repository)]
) -> CatalogoService:
    return CatalogoService(catalogo_repository=catalogo_repository)

catalogo_service_dep = Annotated[CatalogoService, Depends(get_catalogo_service)]