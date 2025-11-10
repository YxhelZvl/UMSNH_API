# src/app/features/laboratorios/domain/entities/laboratorio.py
from pydantic import BaseModel
from typing import Optional
from src.app.features.laboratorios.domain.value_objects.nombre_laboratorio import NombreLaboratorio
from src.app.features.laboratorios.domain.value_objects.ubicacion_laboratorio import UbicacionLaboratorio

class Laboratorio(BaseModel):
    id_laboratorio: Optional[int] = None
    nombre: NombreLaboratorio
    ubicacion: UbicacionLaboratorio
    responsable_id: Optional[int] = None

    def cambiar_nombre(self, nuevo_nombre: str):
        """Método de negocio para cambiar nombre"""
        self.nombre = NombreLaboratorio(valor=nuevo_nombre)
    
    def cambiar_ubicacion(self, nueva_ubicacion: str):
        """Método de negocio para cambiar ubicación"""
        self.ubicacion = UbicacionLaboratorio(valor=nueva_ubicacion)
    
    def asignar_responsable(self, id_responsable: int):
        """Método de negocio para asignar responsable"""
        self.responsable_id = id_responsable
    
    def remover_responsable(self):
        """Método de negocio para remover responsable"""
        self.responsable_id = None
    
    def tiene_responsable(self) -> bool:
        """Método de negocio: verifica si tiene responsable asignado"""
        return self.responsable_id is not None

    class Config:
        arbitrary_types_allowed = True