# src/app/features/laboratorios/domain/repositories/laboratorio_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.laboratorios.domain.entities.laboratorio import Laboratorio

class LaboratorioRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Laboratorio]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_laboratorio: int) -> Optional[Laboratorio]:
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Laboratorio]:
        pass
    
    @abstractmethod
    def get_by_responsable(self, responsable_id: int) -> List[Laboratorio]:
        pass
    
    @abstractmethod
    def create(self, laboratorio: Laboratorio) -> Laboratorio:
        pass
    
    @abstractmethod
    def update(self, id_laboratorio: int, laboratorio: Laboratorio) -> Optional[Laboratorio]:
        pass
    
    @abstractmethod
    def delete(self, id_laboratorio: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_nombre(self, nombre: str) -> bool:
        pass

    # Métodos para datos detallados con JOINs
    @abstractmethod
    def get_all_with_details(self) -> List[dict]:
        pass

    @abstractmethod
    def get_by_id_with_details(self, id_laboratorio: int) -> Optional[dict]:
        pass

    @abstractmethod
    def get_by_responsable_with_details(self, responsable_id: int) -> List[dict]:
        pass

    @abstractmethod
    def get_by_nombre_with_details(self, nombre: str) -> Optional[dict]:
        pass