# src/app/features/maestros/domain/repositories/maestro_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.maestros.domain.entities.maestro import Maestro

class MaestroRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Maestro]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_maestro: int) -> Optional[Maestro]:
        pass
    
    @abstractmethod
    def get_by_usuario_id(self, id_usuario: int) -> Optional[Maestro]:
        pass
    
    @abstractmethod
    def create(self, maestro: Maestro) -> Maestro:
        pass
    
    @abstractmethod
    def update(self, id_maestro: int, maestro: Maestro) -> Optional[Maestro]:
        pass
    
    @abstractmethod
    def delete(self, id_maestro: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_usuario_id(self, id_usuario: int) -> bool:
        pass

    # Métodos para datos detallados con JOINs
    @abstractmethod
    def get_all_with_details(self) -> List[dict]:
        pass

    @abstractmethod
    def get_by_id_with_details(self, id_maestro: int) -> Optional[dict]:
        pass

    @abstractmethod
    def get_by_usuario_id_with_details(self, id_usuario: int) -> Optional[dict]:
        pass