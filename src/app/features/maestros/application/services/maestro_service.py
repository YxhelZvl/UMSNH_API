# src/app/features/maestros/application/services/maestro_service.py
from typing import List, Optional
from src.app.features.maestros.domain.entities.maestro import Maestro
from src.app.features.maestros.domain.repositories.maestro_repository import MaestroRepository
from src.app.features.maestros.application.dtos import CreateMaestroDTO, UpdateMaestroDTO

# Importamos los servicios/repositorios de las dependencias
from src.app.features.user.domain.repositories.user_repository import UserRepository

class MaestroService:
    def __init__(
        self, 
        maestro_repository: MaestroRepository,
        user_repository: UserRepository
    ):
        self.maestro_repository = maestro_repository
        self.user_repository = user_repository
    
    def get_all(self) -> List[Maestro]:
        return self.maestro_repository.get_all()
    
    def get_by_id(self, id_maestro: int) -> Optional[Maestro]:
        return self.maestro_repository.get_by_id(id_maestro)
    
    def get_by_usuario_id(self, id_usuario: int) -> Optional[Maestro]:
        return self.maestro_repository.get_by_usuario_id(id_usuario)
    
    def create(self, create_dto: CreateMaestroDTO) -> Maestro:
        # Validar que el usuario existe
        usuario = self.user_repository.get_by_id(create_dto.id_usuario)
        if not usuario:
            raise ValueError(f"Usuario con ID {create_dto.id_usuario} no encontrado")
        
        # Validar que no exista ya un maestro para este usuario
        existing_maestro = self.maestro_repository.get_by_usuario_id(create_dto.id_usuario)
        if existing_maestro:
            raise ValueError(f"Ya existe un maestro para el usuario con ID {create_dto.id_usuario}")
        
        # Crear la entidad
        maestro = Maestro(
            id_maestro=None,
            id_usuario=create_dto.id_usuario
        )
        
        return self.maestro_repository.create(maestro)
    
    def update(self, id_maestro: int, update_dto: UpdateMaestroDTO) -> Optional[Maestro]:
        # En esta versión simple no hay campos para actualizar
        existing_maestro = self.maestro_repository.get_by_id(id_maestro)
        if not existing_maestro:
            raise ValueError(f"Maestro con ID {id_maestro} no encontrado")
        
        return existing_maestro
    
    def delete(self, id_maestro: int) -> bool:
        existing_maestro = self.maestro_repository.get_by_id(id_maestro)
        if not existing_maestro:
            raise ValueError(f"Maestro con ID {id_maestro} no encontrado")
        
        return self.maestro_repository.delete(id_maestro)
    
    def exists_by_usuario_id(self, id_usuario: int) -> bool:
        return self.maestro_repository.exists_by_usuario_id(id_usuario)

    # Métodos para datos detallados
    def get_all_with_details(self) -> List[dict]:
        return self.maestro_repository.get_all_with_details()

    def get_by_id_with_details(self, id_maestro: int) -> Optional[dict]:
        return self.maestro_repository.get_by_id_with_details(id_maestro)

    def get_by_usuario_id_with_details(self, id_usuario: int) -> Optional[dict]:
        return self.maestro_repository.get_by_usuario_id_with_details(id_usuario)