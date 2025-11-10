# src/app/features/rol/infrastructure/mappers/rol_mapper.py
from src.app.features.rol.domain.entities.rol import Rol
from src.app.features.rol.domain.value_objects.tipo_rol import TipoRolValueObject
from src.app.features.rol.infrastructure.models.rol_model import RolDB

class RolMapper:
    """Mapper para convertir entre la entidad de dominio Rol y el modelo de BD RolDB"""

    @staticmethod
    def to_domain(rol_db: RolDB) -> Rol:
        """Convierte RolDB (modelo de BD) a Rol (entidad de dominio)"""
        if not rol_db:
            return None
            
        return Rol(
            id_rol=rol_db.id_rol,
            tipo_rol=TipoRolValueObject(valor=rol_db.tipo_rol)
        )

    @staticmethod
    def to_db(rol: Rol) -> RolDB:
        """Convierte Rol (entidad de dominio) a RolDB (modelo de BD)"""
        if not rol:
            return None
            
        return RolDB(
            id_rol=rol.id_rol,
            tipo_rol=rol.tipo_rol.valor  # Extraemos el string del Value Object
        )