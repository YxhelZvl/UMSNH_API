# src/app/features/carrera/application/services/carrera_service.py
from typing import List, Optional
from src.app.features.carrera.domain.entities.carrera import Carrera
from src.app.features.carrera.domain.value_objects.nombre_carrera import NombreCarreraValueObject
from src.app.features.carrera.domain.value_objects.facultad import FacultadValueObject
from src.app.features.carrera.domain.repositories.carrera_repository import CarreraRepository
from src.app.features.carrera.application.dtos import CreateCarreraDTO, UpdateCarreraDTO

class CarreraService:
    def __init__(self, carrera_repository: CarreraRepository):
        self.carrera_repository = carrera_repository
    
    def get_all(self) -> List[Carrera]:
        return self.carrera_repository.get_all()
    
    def get_by_id(self, id_carrera: int) -> Optional[Carrera]:
        return self.carrera_repository.get_by_id(id_carrera)
    
    def get_by_nombre(self, nombre_carrera: str) -> Optional[Carrera]:
        return self.carrera_repository.get_by_nombre(nombre_carrera)
    
    def create(self, create_dto: CreateCarreraDTO) -> Carrera:
        # Verificar si ya existe una carrera con el mismo nombre
        existing_carrera = self.carrera_repository.get_by_nombre(create_dto.carrera)
        if existing_carrera:
            raise ValueError(f"Ya existe una carrera con el nombre: {create_dto.carrera}")
        
        # Crear la entidad de dominio
        carrera = Carrera(
            id_carrera=None,
            carrera=NombreCarreraValueObject(valor=create_dto.carrera),
            facultad=FacultadValueObject(valor=create_dto.facultad)
        )
        
        return self.carrera_repository.create(carrera)
    
    def update(self, id_carrera: int, update_dto: UpdateCarreraDTO) -> Optional[Carrera]:
        existing_carrera = self.carrera_repository.get_by_id(id_carrera)
        if not existing_carrera:
            raise ValueError(f"Carrera con ID {id_carrera} no encontrada")
        
        # Si se está cambiando el nombre, verificar que no exista otra con el mismo nombre
        if update_dto.carrera and update_dto.carrera != existing_carrera.carrera.valor:
            carrera_con_mismo_nombre = self.carrera_repository.get_by_nombre(update_dto.carrera)
            if carrera_con_mismo_nombre and carrera_con_mismo_nombre.id_carrera != id_carrera:
                raise ValueError(f"Ya existe una carrera con el nombre: {update_dto.carrera}")
        
        # Aplicar cambios
        if update_dto.carrera:
            existing_carrera.cambiar_nombre(update_dto.carrera)
        
        if update_dto.facultad:
            existing_carrera.cambiar_facultad(update_dto.facultad)
        
        return self.carrera_repository.update(id_carrera, existing_carrera)
    
    def delete(self, id_carrera: int) -> bool:
        existing_carrera = self.carrera_repository.get_by_id(id_carrera)
        if not existing_carrera:
            raise ValueError(f"Carrera con ID {id_carrera} no encontrada")
        
        # Aquí podrías agregar validaciones adicionales
        # Por ejemplo: verificar que no haya estudiantes en esta carrera
        
        return self.carrera_repository.delete(id_carrera)
    
    def exists_by_nombre(self, nombre_carrera: str) -> bool:
        return self.carrera_repository.exists_by_nombre(nombre_carrera)