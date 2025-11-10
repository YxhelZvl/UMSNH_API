# src/app/features/ciclo/domain/repositories/ciclo_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from src.app.features.ciclo.domain.entities.ciclo import Ciclo

class CicloRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Ciclo]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_ciclo: int) -> Optional[Ciclo]:
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre_ciclo: str) -> Optional[Ciclo]:
        pass
    
    @abstractmethod
    def get_ciclos_activos(self) -> List[Ciclo]:
        pass
    
    @abstractmethod
    def get_ciclos_por_fecha(self, fecha: date) -> List[Ciclo]:
        pass
    
    @abstractmethod
    def create(self, ciclo: Ciclo) -> Ciclo:
        pass
    
    @abstractmethod
    def update(self, id_ciclo: int, ciclo: Ciclo) -> Optional[Ciclo]:
        pass
    
    @abstractmethod
    def delete(self, id_ciclo: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_nombre(self, nombre_ciclo: str) -> bool:
        pass