# src/app/features/administrativo/domain/repositories/administrativo_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.administrativo.domain.entities.administrativo import Administrativo

class AdministrativoRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Administrativo]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_administrativo: int) -> Optional[Administrativo]:
        pass
    
    @abstractmethod
    def get_by_usuario_id(self, id_usuario: int) -> Optional[Administrativo]:
        pass
    
    @abstractmethod
    def get_by_departamento(self, departamento: str) -> List[Administrativo]:
        pass
    
    @abstractmethod
    def create(self, administrativo: Administrativo) -> Administrativo:
        pass
    
    @abstractmethod
    def update(self, id_administrativo: int, administrativo: Administrativo) -> Optional[Administrativo]:
        pass
    
    @abstractmethod
    def delete(self, id_administrativo: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_usuario_id(self, id_usuario: int) -> bool:
        pass

    # Métodos para datos detallados con JOINs
    @abstractmethod
    def get_all_with_details(self) -> List[dict]:
        pass

    @abstractmethod
    def get_by_id_with_details(self, id_administrativo: int) -> Optional[dict]:
        pass

    @abstractmethod
    def get_by_usuario_id_with_details(self, id_usuario: int) -> Optional[dict]:
        pass

    @abstractmethod
    def get_by_departamento_with_details(self, departamento: str) -> List[dict]:
        pass