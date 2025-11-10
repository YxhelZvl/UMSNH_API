# src/app/features/ciclo/domain/entities/ciclo.py
from pydantic import BaseModel
from typing import Optional
from src.app.features.ciclo.domain.value_objects.nombre_ciclo import NombreCicloValueObject
from src.app.features.ciclo.domain.value_objects.rango_fechas import RangoFechasValueObject
from datetime import date
class Ciclo(BaseModel):
    id_ciclo: Optional[int] = None
    ciclo: NombreCicloValueObject
    rango_fechas: RangoFechasValueObject
    
    def cambiar_nombre(self, nuevo_nombre: str):
        """Método de negocio para cambiar el nombre del ciclo"""
        self.ciclo = NombreCicloValueObject(valor=nuevo_nombre)
    
    def cambiar_rango_fechas(self, nueva_fecha_inicio: date, nueva_fecha_final: date):
        """Método de negocio para cambiar el rango de fechas"""
        self.rango_fechas = RangoFechasValueObject(
            fecha_inicio=nueva_fecha_inicio,
            fecha_final=nueva_fecha_final
        )
    
    
    
    class Config:
        arbitrary_types_allowed = True