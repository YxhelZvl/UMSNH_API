# src/app/features/bibliotecas/domain/repositories/biblioteca_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.bibliotecas.domain.entities.biblioteca import Biblioteca

class BibliotecaRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Biblioteca]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_biblioteca: int) -> Optional[Biblioteca]:
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Biblioteca]:
        pass
    
    @abstractmethod
    def create(self, biblioteca: Biblioteca) -> Biblioteca:
        pass
    
    @abstractmethod
    def update(self, id_biblioteca: int, biblioteca: Biblioteca) -> Optional[Biblioteca]:
        pass
    
    @abstractmethod
    def delete(self, id_biblioteca: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_nombre(self, nombre: str) -> bool:
        pass