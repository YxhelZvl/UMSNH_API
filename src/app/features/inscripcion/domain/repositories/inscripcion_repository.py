# src/app/features/inscripcion/domain/repositories/inscripcion_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.inscripcion.domain.entities.inscripcion import Inscripcion

class InscripcionRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Inscripcion]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_inscripcion: int) -> Optional[Inscripcion]:
        pass
    
    @abstractmethod
    def get_by_usuario_id(self, id_usuario: int) -> List[Inscripcion]:
        pass
    
    @abstractmethod
    def get_by_ciclo_id(self, id_ciclo: int) -> List[Inscripcion]:
        pass
    
    @abstractmethod
    def get_inscripciones_activas_by_usuario(self, id_usuario: int) -> List[Inscripcion]:
        pass
    
    @abstractmethod
    def create(self, inscripcion: Inscripcion) -> Inscripcion:
        pass
    
    @abstractmethod
    def update(self, id_inscripcion: int, inscripcion: Inscripcion) -> Optional[Inscripcion]:
        pass
    
    @abstractmethod
    def delete(self, id_inscripcion: int) -> bool:
        pass
    
    @abstractmethod
    def exists_inscripcion_activa(self, id_usuario: int, id_ciclo: int) -> bool:
        pass
    
    @abstractmethod
    def get_inscripciones_by_usuario_and_ciclo(self, id_usuario: int, id_ciclo: int) -> List[Inscripcion]:
        pass