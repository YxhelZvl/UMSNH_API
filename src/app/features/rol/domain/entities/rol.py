# src/app/features/rol/domain/entities/rol.py
from pydantic import BaseModel
from typing import Optional
from src.app.features.rol.domain.value_objects.tipo_rol import TipoRolValueObject

class Rol(BaseModel):
    id_rol: Optional[int] = None
    tipo_rol: TipoRolValueObject
    
    def cambiar_tipo_rol(self, nuevo_tipo: str):
        """Método de negocio para cambiar el tipo de rol"""
        self.tipo_rol = TipoRolValueObject(valor=nuevo_tipo)
    
    def es_rol_sistema(self) -> bool:
        """Método de negocio: verifica si es un rol del sistema base"""
        roles_sistema = {"Estudiante", "Maestro", "Administrativo", "Bibliotecario"}
        return str(self.tipo_rol) in roles_sistema
    
    class Config:
        arbitrary_types_allowed = True