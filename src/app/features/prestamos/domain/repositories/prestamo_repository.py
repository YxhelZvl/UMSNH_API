# src/app/features/prestamos/domain/repositories/prestamo_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.prestamos.domain.entities.prestamo import Prestamo

class PrestamoRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Prestamo]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_prestamo: int) -> Optional[Prestamo]:
        pass
    
    @abstractmethod
    def get_by_usuario(self, id_usuario: int) -> List[Prestamo]:
        pass
    
    @abstractmethod
    def get_by_ejemplar(self, id_ejemplar: int) -> List[Prestamo]:
        pass
    
    @abstractmethod
    def get_by_estado(self, estado: str) -> List[Prestamo]:
        pass
    
    @abstractmethod
    def get_prestamos_activos(self) -> List[Prestamo]:
        pass
    
    @abstractmethod
    def get_prestamos_retrasados(self) -> List[Prestamo]:
        pass
    
    @abstractmethod
    def get_prestamos_por_vencer(self, dias: int = 3) -> List[Prestamo]:
        pass
    
    @abstractmethod
    def create(self, prestamo: Prestamo) -> Prestamo:
        pass
    
    @abstractmethod
    def update(self, id_prestamo: int, prestamo: Prestamo) -> Optional[Prestamo]:
        pass
    
    @abstractmethod
    def delete(self, id_prestamo: int) -> bool:
        pass

    # Métodos para datos detallados con JOINs
    @abstractmethod
    def get_all_with_details(self) -> List[dict]:
        pass

    @abstractmethod
    def get_by_id_with_details(self, id_prestamo: int) -> Optional[dict]:
        pass

    @abstractmethod
    def get_by_usuario_with_details(self, id_usuario: int) -> List[dict]:
        pass

    @abstractmethod
    def get_prestamos_activos_with_details(self) -> List[dict]:
        pass