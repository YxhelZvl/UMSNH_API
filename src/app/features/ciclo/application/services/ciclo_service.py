# src/app/features/ciclo/application/services/ciclo_service.py
from typing import List, Optional
from datetime import date
from src.app.features.ciclo.domain.entities.ciclo import Ciclo
from src.app.features.ciclo.domain.value_objects.nombre_ciclo import NombreCicloValueObject
from src.app.features.ciclo.domain.value_objects.rango_fechas import RangoFechasValueObject
from src.app.features.ciclo.domain.repositories.ciclo_repository import CicloRepository
from src.app.features.ciclo.application.dtos import CreateCicloDTO, UpdateCicloDTO

class CicloService:
    def __init__(self, ciclo_repository: CicloRepository):
        self.ciclo_repository = ciclo_repository
    
    def get_all(self) -> List[Ciclo]:
        return self.ciclo_repository.get_all()
    
    def get_by_id(self, id_ciclo: int) -> Optional[Ciclo]:
        return self.ciclo_repository.get_by_id(id_ciclo)
    
    def get_by_nombre(self, nombre_ciclo: str) -> Optional[Ciclo]:
        return self.ciclo_repository.get_by_nombre(nombre_ciclo)
    
    def get_ciclos_activos(self) -> List[Ciclo]:
        return self.ciclo_repository.get_ciclos_activos()
    
    def get_ciclos_por_fecha(self, fecha: date) -> List[Ciclo]:
        return self.ciclo_repository.get_ciclos_por_fecha(fecha)
    
    def create(self, create_dto: CreateCicloDTO) -> Ciclo:
        # Verificar si ya existe un ciclo con el mismo nombre
        existing_ciclo = self.ciclo_repository.get_by_nombre(create_dto.ciclo)
        if existing_ciclo:
            raise ValueError(f"Ya existe un ciclo con el nombre: {create_dto.ciclo}")
        
        # Crear Value Objects
        nombre_ciclo_vo = NombreCicloValueObject(valor=create_dto.ciclo)
        rango_fechas_vo = RangoFechasValueObject(
            fecha_inicio=create_dto.fecha_inicio,
            fecha_final=create_dto.fecha_final
        )
        
        # Crear la entidad de dominio
        ciclo = Ciclo(
            id_ciclo=None,
            ciclo=nombre_ciclo_vo,
            rango_fechas=rango_fechas_vo
        )
        
        return self.ciclo_repository.create(ciclo)
    
    def update(self, id_ciclo: int, update_dto: UpdateCicloDTO) -> Optional[Ciclo]:
        existing_ciclo = self.ciclo_repository.get_by_id(id_ciclo)
        if not existing_ciclo:
            raise ValueError(f"Ciclo con ID {id_ciclo} no encontrado")
        
        # Si se está cambiando el nombre, verificar que no exista otro con el mismo nombre
        if update_dto.ciclo and update_dto.ciclo != existing_ciclo.ciclo.valor:
            ciclo_con_mismo_nombre = self.ciclo_repository.get_by_nombre(update_dto.ciclo)
            if ciclo_con_mismo_nombre and ciclo_con_mismo_nombre.id_ciclo != id_ciclo:
                raise ValueError(f"Ya existe un ciclo con el nombre: {update_dto.ciclo}")
        
        # Aplicar cambios
        if update_dto.ciclo:
            existing_ciclo.cambiar_nombre(update_dto.ciclo)
        
        if update_dto.fecha_inicio or update_dto.fecha_final:
            nueva_fecha_inicio = update_dto.fecha_inicio or existing_ciclo.rango_fechas.fecha_inicio
            nueva_fecha_final = update_dto.fecha_final or existing_ciclo.rango_fechas.fecha_final
            existing_ciclo.cambiar_rango_fechas(nueva_fecha_inicio, nueva_fecha_final)
        
        return self.ciclo_repository.update(id_ciclo, existing_ciclo)
    
    def delete(self, id_ciclo: int) -> bool:
        existing_ciclo = self.ciclo_repository.get_by_id(id_ciclo)
        if not existing_ciclo:
            raise ValueError(f"Ciclo con ID {id_ciclo} no encontrado")
        
        # Aquí podrías agregar validaciones adicionales
        # Por ejemplo: verificar que no haya inscripciones en este ciclo
        
        return self.ciclo_repository.delete(id_ciclo)
    
    def exists_by_nombre(self, nombre_ciclo: str) -> bool:
        return self.ciclo_repository.exists_by_nombre(nombre_ciclo)
    
