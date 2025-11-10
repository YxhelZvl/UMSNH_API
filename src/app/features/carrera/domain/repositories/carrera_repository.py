# src/app/features/carrera/domain/repositories/carrera_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.carrera.domain.entities.carrera import Carrera

class CarreraRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Carrera]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_carrera: int) -> Optional[Carrera]:
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre_carrera: str) -> Optional[Carrera]:
        pass
    
    @abstractmethod
    def create(self, carrera: Carrera) -> Carrera:
        pass
    
    @abstractmethod
    def update(self, id_carrera: int, carrera: Carrera) -> Optional[Carrera]:
        pass
    
    @abstractmethod
    def delete(self, id_carrera: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_nombre(self, nombre_carrera: str) -> bool:
        pass