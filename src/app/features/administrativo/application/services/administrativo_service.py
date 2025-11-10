# src/app/features/administrativo/application/services/administrativo_service.py
from typing import List, Optional
from src.app.features.administrativo.domain.entities.administrativo import Administrativo
from src.app.features.administrativo.domain.repositories.administrativo_repository import AdministrativoRepository
from src.app.features.administrativo.application.dtos import CreateAdministrativoDTO, UpdateAdministrativoDTO

# Importamos los servicios/repositorios de las dependencias
from src.app.features.user.domain.repositories.user_repository import UserRepository

class AdministrativoService:
    def __init__(
        self, 
        administrativo_repository: AdministrativoRepository,
        user_repository: UserRepository
    ):
        self.administrativo_repository = administrativo_repository
        self.user_repository = user_repository
    
    def get_all(self) -> List[Administrativo]:
        return self.administrativo_repository.get_all()
    
    def get_by_id(self, id_administrativo: int) -> Optional[Administrativo]:
        return self.administrativo_repository.get_by_id(id_administrativo)
    
    def get_by_usuario_id(self, id_usuario: int) -> Optional[Administrativo]:
        return self.administrativo_repository.get_by_usuario_id(id_usuario)
    
    def get_by_departamento(self, departamento: str) -> List[Administrativo]:
        return self.administrativo_repository.get_by_departamento(departamento)
    
    def create(self, create_dto: CreateAdministrativoDTO) -> Administrativo:
        # Validar que el usuario existe
        usuario = self.user_repository.get_by_id(create_dto.id_usuario)
        if not usuario:
            raise ValueError(f"Usuario con ID {create_dto.id_usuario} no encontrado")
        
        # Validar que no exista ya un administrativo para este usuario
        existing_administrativo = self.administrativo_repository.get_by_usuario_id(create_dto.id_usuario)
        if existing_administrativo:
            raise ValueError(f"Ya existe un administrativo para el usuario con ID {create_dto.id_usuario}")
        
        # Crear la entidad
        administrativo = Administrativo(
            id_administrativo=None,
            id_usuario=create_dto.id_usuario,
            departamento=create_dto.departamento
        )
        
        return self.administrativo_repository.create(administrativo)
    
    def update(self, id_administrativo: int, update_dto: UpdateAdministrativoDTO) -> Optional[Administrativo]:
        existing_administrativo = self.administrativo_repository.get_by_id(id_administrativo)
        if not existing_administrativo:
            raise ValueError(f"Administrativo con ID {id_administrativo} no encontrado")
        
        # Aplicar cambios
        if update_dto.departamento is not None:
            existing_administrativo.departamento = update_dto.departamento
        
        return self.administrativo_repository.update(id_administrativo, existing_administrativo)
    
    def delete(self, id_administrativo: int) -> bool:
        existing_administrativo = self.administrativo_repository.get_by_id(id_administrativo)
        if not existing_administrativo:
            raise ValueError(f"Administrativo con ID {id_administrativo} no encontrado")
        
        return self.administrativo_repository.delete(id_administrativo)
    
    def exists_by_usuario_id(self, id_usuario: int) -> bool:
        return self.administrativo_repository.exists_by_usuario_id(id_usuario)

    # Métodos para datos detallados
    def get_all_with_details(self) -> List[dict]:
        return self.administrativo_repository.get_all_with_details()

    def get_by_id_with_details(self, id_administrativo: int) -> Optional[dict]:
        return self.administrativo_repository.get_by_id_with_details(id_administrativo)

    def get_by_usuario_id_with_details(self, id_usuario: int) -> Optional[dict]:
        return self.administrativo_repository.get_by_usuario_id_with_details(id_usuario)

    def get_by_departamento_with_details(self, departamento: str) -> List[dict]:
        return self.administrativo_repository.get_by_departamento_with_details(departamento)