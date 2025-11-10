# src/app/features/carrera/domain/entities/carrera.py
from pydantic import BaseModel
from typing import Optional
from src.app.features.carrera.domain.value_objects.nombre_carrera import NombreCarreraValueObject
from src.app.features.carrera.domain.value_objects.facultad import FacultadValueObject

class Carrera(BaseModel):
    id_carrera: Optional[int] = None
    carrera: NombreCarreraValueObject
    facultad: FacultadValueObject
    
    def cambiar_nombre(self, nuevo_nombre: str):
        """Método de negocio para cambiar el nombre de la carrera"""
        self.carrera = NombreCarreraValueObject(valor=nuevo_nombre)
    
    def cambiar_facultad(self, nueva_facultad: str):
        """Método de negocio para cambiar la facultad"""
        self.facultad = FacultadValueObject(valor=nueva_facultad)
    
    class Config:
        arbitrary_types_allowed = True