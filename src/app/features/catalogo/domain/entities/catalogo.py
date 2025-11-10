# src/app/features/catalogo/domain/entities/catalogo.py
from pydantic import BaseModel
from typing import Optional
from src.app.features.catalogo.domain.value_objects.tipo_item import TipoItem
from src.app.features.catalogo.domain.value_objects.nombre_item import NombreItem
from src.app.features.catalogo.domain.value_objects.isbn import ISBN

class Catalogo(BaseModel):
    id_catalogo: Optional[int] = None
    tipo: TipoItem
    nombre: NombreItem
    autor: Optional[str] = None
    isbn: Optional[ISBN] = None
    descripcion: Optional[str] = None

    def cambiar_nombre(self, nuevo_nombre: str):
        """Método de negocio para cambiar nombre"""
        self.nombre = NombreItem(valor=nuevo_nombre)
    
    def cambiar_tipo(self, nuevo_tipo: str):
        """Método de negocio para cambiar tipo"""
        self.tipo = TipoItem(valor=nuevo_tipo)
    
    def cambiar_autor(self, nuevo_autor: str):
        """Método de negocio para cambiar autor"""
        self.autor = nuevo_autor
    
    def cambiar_isbn(self, nuevo_isbn: str):
        """Método de negocio para cambiar ISBN"""
        self.isbn = ISBN(valor=nuevo_isbn) if nuevo_isbn else None
    
    def cambiar_descripcion(self, nueva_descripcion: str):
        """Método de negocio para cambiar descripción"""
        self.descripcion = nueva_descripcion
    
    def es_libro(self) -> bool:
        """Método de negocio: verifica si es un libro"""
        return self.tipo.es_libro()
    
    def es_herramienta(self) -> bool:
        """Método de negocio: verifica si es una herramienta"""
        return self.tipo.es_herramienta()
    
    def es_equipo(self) -> bool:
        """Método de negocio: verifica si es un equipo"""
        return self.tipo.es_equipo()
    
    def requiere_autor(self) -> bool:
        """Método de negocio: determina si requiere autor"""
        return self.es_libro()
    
    def requiere_isbn(self) -> bool:
        """Método de negocio: determina si requiere ISBN"""
        return self.es_libro()

    class Config:
        arbitrary_types_allowed = True