# src/app/features/rol/infrastructure/dependencies.py
from typing import Annotated
from fastapi import Depends
from src.app.core.database.database import session_dep
from src.app.features.rol.infrastructure.repositories.rol_repository_impl import RolRepositoryImpl
from src.app.features.rol.application.services.rol_service import RolService

def get_rol_repository(session: session_dep) -> RolRepositoryImpl:
    """Provee la implementación concreta del repositorio"""
    return RolRepositoryImpl(session=session)

def get_rol_service(rol_repository: Annotated[RolRepositoryImpl, Depends(get_rol_repository)]) -> RolService:
    """Provee el servicio de aplicación inyectado con el repositorio"""
    return RolService(rol_repository=rol_repository)


# Dependencias tipadas para usar en los routers
rol_repository_dep = Annotated[RolRepositoryImpl, Depends(get_rol_repository)]
rol_service_dep = Annotated[RolService, Depends(get_rol_service)]