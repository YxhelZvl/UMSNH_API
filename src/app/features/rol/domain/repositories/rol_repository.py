# src/app/features/rol/domain/repositories/rol_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.rol.domain.entities.rol import Rol

class RolRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Rol]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_rol: int) -> Optional[Rol]:
        pass
    
    @abstractmethod
    def get_by_tipo(self, tipo_rol: str) -> Optional[Rol]:
        pass
    
    @abstractmethod
    def create(self, rol: Rol) -> Rol:
        pass
    
    @abstractmethod
    def update(self, id_rol: int, rol: Rol) -> Optional[Rol]:
        pass
    
    @abstractmethod
    def delete(self, id_rol: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_tipo(self, tipo_rol: str) -> bool:
        """Verifica si ya existe un rol con ese tipo"""
        pass