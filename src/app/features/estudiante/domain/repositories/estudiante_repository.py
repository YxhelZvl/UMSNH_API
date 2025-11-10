# src/app/features/estudiante/domain/repositories/estudiante_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.estudiante.domain.entities.estudiante import Estudiante

class EstudianteRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Estudiante]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_estudiante: int) -> Optional[Estudiante]:
        pass
    
    @abstractmethod
    def get_by_usuario_id(self, id_usuario: int) -> Optional[Estudiante]:
        pass
    
    @abstractmethod
    def get_by_carrera_id(self, id_carrera: int) -> List[Estudiante]:
        pass
    
    @abstractmethod
    def create(self, estudiante: Estudiante) -> Estudiante:
        pass
    
    @abstractmethod
    def update(self, id_estudiante: int, estudiante: Estudiante) -> Optional[Estudiante]:
        pass
    
    @abstractmethod
    def delete(self, id_estudiante: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_usuario_id(self, id_usuario: int) -> bool:
        pass
    
    @abstractmethod
    def get_all_with_details(self) -> List[dict]:
        pass
    
    @abstractmethod
    def get_by_id_with_details(self, id_estudiante: int) -> Optional[dict]:
        pass
    
    @abstractmethod
    def get_by_usuario_id_with_details(self, id_usuario: int) -> Optional[dict]:
        pass
    
    @abstractmethod
    def get_by_carrera_id_with_details(self, id_carrera: int) -> List[dict]:
        pass