# src/app/features/ejemplares/domain/entities/ejemplar.py
from pydantic import BaseModel
from typing import Optional
from src.app.features.ejemplares.domain.value_objects.codigo_inventario import CodigoInventario
from src.app.features.ejemplares.domain.value_objects.ubicacion_ejemplar import UbicacionEjemplar
from src.app.features.ejemplares.domain.value_objects.estado_ejemplar import EstadoEjemplar

class Ejemplar(BaseModel):
    id_ejemplar: Optional[int] = None
    id_catalogo: int
    codigo_inventario: CodigoInventario
    ubicacion: UbicacionEjemplar
    id_laboratorio: Optional[int] = None
    id_biblioteca: Optional[int] = None
    estado: EstadoEjemplar = EstadoEjemplar(valor="disponible")

    def cambiar_ubicacion_laboratorio(self, id_laboratorio: int):
        """Método de negocio: cambiar a ubicación en laboratorio"""
        self.ubicacion = UbicacionEjemplar(valor="laboratorio")
        self.id_laboratorio = id_laboratorio
        self.id_biblioteca = None
    
    def cambiar_ubicacion_biblioteca(self, id_biblioteca: int):
        """Método de negocio: cambiar a ubicación en biblioteca"""
        self.ubicacion = UbicacionEjemplar(valor="biblioteca")
        self.id_biblioteca = id_biblioteca
        self.id_laboratorio = None
    
    def cambiar_estado(self, nuevo_estado: str):
        """Método de negocio: cambiar estado del ejemplar"""
        self.estado = EstadoEjemplar(valor=nuevo_estado)
    
    def marcar_como_prestado(self):
        """Método de negocio: marcar como prestado"""
        if not self.estado.puede_prestarse():
            raise ValueError(f"No se puede prestar un ejemplar en estado: {self.estado}")
        self.estado = EstadoEjemplar(valor="prestado")
    
    def marcar_como_devuelto(self):
        """Método de negocio: marcar como disponible al devolver"""
        self.estado = EstadoEjemplar(valor="disponible")
    
    def validar_consistencia_ubicacion(self):
        """Método de negocio: validar consistencia entre ubicación y IDs"""
        if self.ubicacion.es_laboratorio() and not self.id_laboratorio:
            raise ValueError("Un ejemplar en laboratorio debe tener id_laboratorio")
        if self.ubicacion.es_biblioteca() and not self.id_biblioteca:
            raise ValueError("Un ejemplar en biblioteca debe tener id_biblioteca")

    class Config:
        arbitrary_types_allowed = True