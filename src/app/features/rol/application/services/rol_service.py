# src/app/features/rol/application/services/rol_service.py
from typing import List, Optional
from src.app.features.rol.domain.entities.rol import Rol
from src.app.features.rol.domain.value_objects.tipo_rol import TipoRolValueObject
from src.app.features.rol.domain.repositories.rol_repository import RolRepository
from src.app.features.rol.application.dtos import CreateRolDTO, UpdateRolDTO

class RolService:
    def __init__(self, rol_repository: RolRepository):
        self.rol_repository = rol_repository
    
    def get_all(self) -> List[Rol]:
        """Obtener todos los roles (devuelve entidades)"""
        return self.rol_repository.get_all()
    
    def get_by_id(self, id_rol: int) -> Optional[Rol]:
        """Obtener rol por ID (devuelve entidad)"""
        return self.rol_repository.get_by_id(id_rol)
    
    def get_by_tipo(self, tipo_rol: str) -> Optional[Rol]:
        """Obtener rol por tipo (devuelve entidad)"""
        return self.rol_repository.get_by_tipo(tipo_rol)
    
    def create(self, create_dto: CreateRolDTO) -> Rol:
        """Crear un nuevo rol (devuelve entidad)"""
        # Verificar si ya existe un rol con el mismo tipo
        existing_rol = self.rol_repository.get_by_tipo(create_dto.tipo_rol)
        if existing_rol:
            raise ValueError(f"Ya existe un rol con el tipo: {create_dto.tipo_rol}")
        
        # Crear la entidad de dominio
        rol = Rol(
            id_rol=None,
            tipo_rol=TipoRolValueObject(valor=create_dto.tipo_rol)
        )
        
        # Guardar a través del repositorio
        return self.rol_repository.create(rol)
    
    def update(self, id_rol: int, update_dto: UpdateRolDTO) -> Optional[Rol]:
        """Actualizar un rol existente (devuelve entidad)"""
        # Verificar que el rol existe
        existing_rol = self.rol_repository.get_by_id(id_rol)
        if not existing_rol:
            raise ValueError(f"Rol con ID {id_rol} no encontrado")
        
        # Verificar si es un rol del sistema (no se pueden modificar)
        if existing_rol.es_rol_sistema():
            raise ValueError("No se pueden modificar los roles del sistema base")
        
        # Si se está cambiando el tipo, verificar que no exista otro con el mismo tipo
        if update_dto.tipo_rol and update_dto.tipo_rol != existing_rol.tipo_rol.valor:
            rol_con_mismo_tipo = self.rol_repository.get_by_tipo(update_dto.tipo_rol)
            if rol_con_mismo_tipo and rol_con_mismo_tipo.id_rol != id_rol:
                raise ValueError(f"Ya existe un rol con el tipo: {update_dto.tipo_rol}")
        
        # Aplicar cambios
        if update_dto.tipo_rol:
            existing_rol.cambiar_tipo_rol(update_dto.tipo_rol)
        
        # Actualizar a través del repositorio
        return self.rol_repository.update(id_rol, existing_rol)
    
    def delete(self, id_rol: int) -> bool:
        """Eliminar un rol (lógico)"""
        # Verificar que el rol existe
        existing_rol = self.rol_repository.get_by_id(id_rol)
        if not existing_rol:
            raise ValueError(f"Rol con ID {id_rol} no encontrado")
        
        # Verificar si es un rol del sistema (no se pueden eliminar)
        if existing_rol.es_rol_sistema():
            raise ValueError("No se pueden eliminar los roles del sistema base")
        
        # Eliminar a través del repositorio
        return self.rol_repository.delete(id_rol)
    
    def exists_by_tipo(self, tipo_rol: str) -> bool:
        """Verificar si existe un rol por tipo"""
        return self.rol_repository.exists_by_tipo(tipo_rol)