# src/app/features/ejemplares/domain/repositories/ejemplar_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.ejemplares.domain.entities.ejemplar import Ejemplar

class EjemplarRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Ejemplar]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_ejemplar: int) -> Optional[Ejemplar]:
        pass
    
    @abstractmethod
    def get_by_codigo_inventario(self, codigo_inventario: str) -> Optional[Ejemplar]:
        pass
    
    @abstractmethod
    def get_by_catalogo(self, id_catalogo: int) -> List[Ejemplar]:
        pass
    
    @abstractmethod
    def get_by_ubicacion(self, ubicacion: str) -> List[Ejemplar]:
        pass
    
    @abstractmethod
    def get_by_estado(self, estado: str) -> List[Ejemplar]:
        pass
    
    @abstractmethod
    def get_by_biblioteca(self, id_biblioteca: int) -> List[Ejemplar]:
        pass
    
    @abstractmethod
    def get_by_laboratorio(self, id_laboratorio: int) -> List[Ejemplar]:
        pass
    
    @abstractmethod
    def create(self, ejemplar: Ejemplar) -> Ejemplar:
        pass
    
    @abstractmethod
    def update(self, id_ejemplar: int, ejemplar: Ejemplar) -> Optional[Ejemplar]:
        pass
    
    @abstractmethod
    def delete(self, id_ejemplar: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_codigo_inventario(self, codigo_inventario: str) -> bool:
        pass

    # Métodos para datos detallados con JOINs
    @abstractmethod
    def get_all_with_details(self) -> List[dict]:
        pass

    @abstractmethod
    def get_by_id_with_details(self, id_ejemplar: int) -> Optional[dict]:
        pass

    @abstractmethod
    def get_disponibles_for_prestamo(self) -> List[dict]:
        pass