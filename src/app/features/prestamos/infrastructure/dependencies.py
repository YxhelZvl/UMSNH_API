# src/app/features/prestamos/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.prestamos.infrastructure.repositories.prestamo_repository_impl import PrestamoRepositoryImpl
from src.app.features.prestamos.application.services.prestamo_service import PrestamoService

# Importar dependencias de las otras features
from src.app.features.user.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.app.features.ejemplares.infrastructure.repositories.ejemplar_repository_impl import EjemplarRepositoryImpl

def get_prestamo_repository(session: session_dep) -> PrestamoRepositoryImpl:
    return PrestamoRepositoryImpl(session=session)

def get_user_repository(session: session_dep) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=session)

def get_ejemplar_repository(session: session_dep) -> EjemplarRepositoryImpl:
    return EjemplarRepositoryImpl(session=session)

def get_prestamo_service(
    prestamo_repository: Annotated[PrestamoRepositoryImpl, Depends(get_prestamo_repository)],
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)],
    ejemplar_repository: Annotated[EjemplarRepositoryImpl, Depends(get_ejemplar_repository)]
) -> PrestamoService:
    return PrestamoService(
        prestamo_repository=prestamo_repository,
        user_repository=user_repository,
        ejemplar_repository=ejemplar_repository
    )

prestamo_service_dep = Annotated[PrestamoService, Depends(get_prestamo_service)]