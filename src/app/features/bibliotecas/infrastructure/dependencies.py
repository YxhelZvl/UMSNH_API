# src/app/features/bibliotecas/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.bibliotecas.infrastructure.repositories.biblioteca_repository_impl import BibliotecaRepositoryImpl
from src.app.features.bibliotecas.application.services.biblioteca_service import BibliotecaService

def get_biblioteca_repository(session: session_dep) -> BibliotecaRepositoryImpl:
    return BibliotecaRepositoryImpl(session=session)

def get_biblioteca_service(
    biblioteca_repository: Annotated[BibliotecaRepositoryImpl, Depends(get_biblioteca_repository)]
) -> BibliotecaService:
    return BibliotecaService(biblioteca_repository=biblioteca_repository)

biblioteca_service_dep = Annotated[BibliotecaService, Depends(get_biblioteca_service)]