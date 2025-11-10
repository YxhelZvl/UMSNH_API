# src/app/features/user/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.user.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.app.features.user.application.services.user_service import UserService

def get_user_repository(session: session_dep) -> UserRepositoryImpl:
    """Provee la implementación concreta del repositorio de User"""
    return UserRepositoryImpl(session=session)

def get_user_service(user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)]) -> UserService:
    """Provee el servicio de aplicación de User inyectado con el repositorio"""
    return UserService(user_repository=user_repository)

# Dependencias tipadas para usar en los routers
user_repository_dep = Annotated[UserRepositoryImpl, Depends(get_user_repository)]
user_service_dep = Annotated[UserService, Depends(get_user_service)]