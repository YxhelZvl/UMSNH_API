# src/app/features/ejemplares/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.ejemplares.infrastructure.repositories.ejemplar_repository_impl import EjemplarRepositoryImpl
from src.app.features.ejemplares.application.services.ejemplar_service import EjemplarService

# Importar dependencias de las otras features
from src.app.features.catalogo.infrastructure.repositories.catalogo_repository_impl import CatalogoRepositoryImpl
from src.app.features.bibliotecas.infrastructure.repositories.biblioteca_repository_impl import BibliotecaRepositoryImpl
from src.app.features.laboratorios.infrastructure.repositories.laboratorio_repository_impl import LaboratorioRepositoryImpl

def get_ejemplar_repository(session: session_dep) -> EjemplarRepositoryImpl:
    return EjemplarRepositoryImpl(session=session)

def get_catalogo_repository(session: session_dep) -> CatalogoRepositoryImpl:
    return CatalogoRepositoryImpl(session=session)

def get_biblioteca_repository(session: session_dep) -> BibliotecaRepositoryImpl:
    return BibliotecaRepositoryImpl(session=session)

def get_laboratorio_repository(session: session_dep) -> LaboratorioRepositoryImpl:
    return LaboratorioRepositoryImpl(session=session)

def get_ejemplar_service(
    ejemplar_repository: Annotated[EjemplarRepositoryImpl, Depends(get_ejemplar_repository)],
    catalogo_repository: Annotated[CatalogoRepositoryImpl, Depends(get_catalogo_repository)],
    biblioteca_repository: Annotated[BibliotecaRepositoryImpl, Depends(get_biblioteca_repository)],
    laboratorio_repository: Annotated[LaboratorioRepositoryImpl, Depends(get_laboratorio_repository)]
) -> EjemplarService:
    return EjemplarService(
        ejemplar_repository=ejemplar_repository,
        catalogo_repository=catalogo_repository,
        biblioteca_repository=biblioteca_repository,
        laboratorio_repository=laboratorio_repository
    )

ejemplar_service_dep = Annotated[EjemplarService, Depends(get_ejemplar_service)]