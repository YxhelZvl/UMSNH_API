# src/app/features/catalogo/domain/repositories/catalogo_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.catalogo.domain.entities.catalogo import Catalogo

class CatalogoRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Catalogo]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_catalogo: int) -> Optional[Catalogo]:
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Catalogo]:
        pass
    
    @abstractmethod
    def get_by_tipo(self, tipo: str) -> List[Catalogo]:
        pass
    
    @abstractmethod
    def get_by_autor(self, autor: str) -> List[Catalogo]:
        pass
    
    @abstractmethod
    def get_by_isbn(self, isbn: str) -> Optional[Catalogo]:
        pass
    
    @abstractmethod
    def create(self, catalogo: Catalogo) -> Catalogo:
        pass
    
    @abstractmethod
    def update(self, id_catalogo: int, catalogo: Catalogo) -> Optional[Catalogo]:
        pass
    
    @abstractmethod
    def delete(self, id_catalogo: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_nombre(self, nombre: str) -> bool:
        pass
    
    @abstractmethod
    def exists_by_isbn(self, isbn: str) -> bool:
        pass

    # Métodos para tipos específicos
    @abstractmethod
    def get_libros(self) -> List[Catalogo]:
        pass

    @abstractmethod
    def get_herramientas(self) -> List[Catalogo]:
        pass

    @abstractmethod
    def get_equipos(self) -> List[Catalogo]:
        pass