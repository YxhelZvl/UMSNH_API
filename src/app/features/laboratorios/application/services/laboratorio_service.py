# src/app/features/laboratorios/application/services/laboratorio_service.py
from typing import List, Optional
from src.app.features.laboratorios.domain.entities.laboratorio import Laboratorio
from src.app.features.laboratorios.domain.repositories.laboratorio_repository import LaboratorioRepository
from src.app.features.laboratorios.application.dtos import CreateLaboratorioDTO, UpdateLaboratorioDTO
from src.app.features.laboratorios.domain.value_objects.nombre_laboratorio import NombreLaboratorio
from src.app.features.laboratorios.domain.value_objects.ubicacion_laboratorio import UbicacionLaboratorio

# Importamos los servicios/repositorios de las dependencias
from src.app.features.user.domain.repositories.user_repository import UserRepository

class LaboratorioService:
    def __init__(
        self, 
        laboratorio_repository: LaboratorioRepository,
        user_repository: UserRepository
    ):
        self.laboratorio_repository = laboratorio_repository
        self.user_repository = user_repository
    
    def get_all(self) -> List[Laboratorio]:
        return self.laboratorio_repository.get_all()
    
    def get_by_id(self, id_laboratorio: int) -> Optional[Laboratorio]:
        return self.laboratorio_repository.get_by_id(id_laboratorio)
    
    def get_by_nombre(self, nombre: str) -> Optional[Laboratorio]:
        return self.laboratorio_repository.get_by_nombre(nombre)
    
    def get_by_responsable(self, responsable_id: int) -> List[Laboratorio]:
        return self.laboratorio_repository.get_by_responsable(responsable_id)
    
    def create(self, create_dto: CreateLaboratorioDTO) -> Laboratorio:
        # Validar que no exista un laboratorio con el mismo nombre
        existing_laboratorio = self.laboratorio_repository.get_by_nombre(create_dto.nombre)
        if existing_laboratorio:
            raise ValueError(f"Ya existe un laboratorio con el nombre: {create_dto.nombre}")
        
        # Validar que el responsable existe (si se proporciona)
        if create_dto.responsable_id:
            usuario = self.user_repository.get_by_id(create_dto.responsable_id)
            if not usuario:
                raise ValueError(f"Usuario responsable con ID {create_dto.responsable_id} no encontrado")
        
        # Crear los value objects
        nombre_vo = NombreLaboratorio(valor=create_dto.nombre)
        ubicacion_vo = UbicacionLaboratorio(valor=create_dto.ubicacion)
        
        # Crear la entidad
        laboratorio = Laboratorio(
            id_laboratorio=None,
            nombre=nombre_vo,
            ubicacion=ubicacion_vo,
            responsable_id=create_dto.responsable_id
        )
        
        return self.laboratorio_repository.create(laboratorio)
    
    def update(self, id_laboratorio: int, update_dto: UpdateLaboratorioDTO) -> Optional[Laboratorio]:
        existing_laboratorio = self.laboratorio_repository.get_by_id(id_laboratorio)
        if not existing_laboratorio:
            raise ValueError(f"Laboratorio con ID {id_laboratorio} no encontrado")
        
        # Verificar si se está cambiando el nombre y si ya existe otro con el mismo nombre
        if update_dto.nombre is not None and update_dto.nombre != existing_laboratorio.nombre.valor:
            laboratorio_con_mismo_nombre = self.laboratorio_repository.get_by_nombre(update_dto.nombre)
            if laboratorio_con_mismo_nombre:
                raise ValueError(f"Ya existe un laboratorio con el nombre: {update_dto.nombre}")
        
        # Validar que el responsable existe (si se está cambiando)
        if update_dto.responsable_id is not None and update_dto.responsable_id != existing_laboratorio.responsable_id:
            if update_dto.responsable_id != 0:  # 0 significa remover responsable
                usuario = self.user_repository.get_by_id(update_dto.responsable_id)
                if not usuario:
                    raise ValueError(f"Usuario responsable con ID {update_dto.responsable_id} no encontrado")
        
        # Actualizar campos
        if update_dto.nombre is not None:
            existing_laboratorio.nombre = NombreLaboratorio(valor=update_dto.nombre)
        if update_dto.ubicacion is not None:
            existing_laboratorio.ubicacion = UbicacionLaboratorio(valor=update_dto.ubicacion)
        if update_dto.responsable_id is not None:
            existing_laboratorio.responsable_id = update_dto.responsable_id if update_dto.responsable_id != 0 else None
        
        return self.laboratorio_repository.update(id_laboratorio, existing_laboratorio)
    
    def delete(self, id_laboratorio: int) -> bool:
        existing_laboratorio = self.laboratorio_repository.get_by_id(id_laboratorio)
        if not existing_laboratorio:
            raise ValueError(f"Laboratorio con ID {id_laboratorio} no encontrado")
        
        return self.laboratorio_repository.delete(id_laboratorio)
    
    def exists_by_nombre(self, nombre: str) -> bool:
        return self.laboratorio_repository.exists_by_nombre(nombre)

    # Métodos para datos detallados
    def get_all_with_details(self) -> List[dict]:
        return self.laboratorio_repository.get_all_with_details()

    def get_by_id_with_details(self, id_laboratorio: int) -> Optional[dict]:
        return self.laboratorio_repository.get_by_id_with_details(id_laboratorio)

    def get_by_responsable_with_details(self, responsable_id: int) -> List[dict]:
        return self.laboratorio_repository.get_by_responsable_with_details(responsable_id)

    def get_by_nombre_with_details(self, nombre: str) -> Optional[dict]:
        return self.laboratorio_repository.get_by_nombre_with_details(nombre)