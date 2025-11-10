# src/app/features/inscripcion/application/services/inscripcion_service.py
from typing import List, Optional
from datetime import date
from src.app.features.inscripcion.domain.entities.inscripcion import Inscripcion
from src.app.features.inscripcion.domain.value_objects.estado_inscripcion import EstadoInscripcionValueObject, EstadoInscripcionEnum
from src.app.features.inscripcion.domain.repositories.inscripcion_repository import InscripcionRepository
from src.app.features.inscripcion.application.dtos import CreateInscripcionDTO, UpdateInscripcionDTO

# Importamos los servicios/repositorios de las dependencias
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.features.ciclo.domain.repositories.ciclo_repository import CicloRepository

class InscripcionService:
    def __init__(
        self, 
        inscripcion_repository: InscripcionRepository,
        user_repository: UserRepository,
        ciclo_repository: CicloRepository
    ):
        self.inscripcion_repository = inscripcion_repository
        self.user_repository = user_repository
        self.ciclo_repository = ciclo_repository
    
    def get_all(self) -> List[Inscripcion]:
        return self.inscripcion_repository.get_all()
    
    def get_by_id(self, id_inscripcion: int) -> Optional[Inscripcion]:
        return self.inscripcion_repository.get_by_id(id_inscripcion)
    
    def get_by_usuario_id(self, id_usuario: int) -> List[Inscripcion]:
        return self.inscripcion_repository.get_by_usuario_id(id_usuario)
    
    def get_by_ciclo_id(self, id_ciclo: int) -> List[Inscripcion]:
        return self.inscripcion_repository.get_by_ciclo_id(id_ciclo)
    
    def get_inscripciones_activas_by_usuario(self, id_usuario: int) -> List[Inscripcion]:
        return self.inscripcion_repository.get_inscripciones_activas_by_usuario(id_usuario)
    
    def create(self, create_dto: CreateInscripcionDTO) -> Inscripcion:
        # Validar que el usuario existe
        usuario = self.user_repository.get_by_id(create_dto.id_usuario)
        if not usuario:
            raise ValueError(f"Usuario con ID {create_dto.id_usuario} no encontrado")
        
        # Validar que el ciclo existe
        ciclo = self.ciclo_repository.get_by_id(create_dto.id_ciclo)
        if not ciclo:
            raise ValueError(f"Ciclo con ID {create_dto.id_ciclo} no encontrado")
        
        # Validar que no exista ya una inscripción activa para este usuario y ciclo
        if self.inscripcion_repository.exists_inscripcion_activa(create_dto.id_usuario, create_dto.id_ciclo):
            raise ValueError(f"El usuario ya tiene una inscripción activa en este ciclo")
        
        # Crear la entidad
        inscripcion = Inscripcion(
            id_inscripcion=None,
            id_usuario=create_dto.id_usuario,
            id_ciclo=create_dto.id_ciclo,
            fecha_inscripcion=create_dto.fecha_inscripcion,
            estado=EstadoInscripcionValueObject(valor=create_dto.estado)
        )
        
        return self.inscripcion_repository.create(inscripcion)
    
    def update(self, id_inscripcion: int, update_dto: UpdateInscripcionDTO) -> Optional[Inscripcion]:
        existing_inscripcion = self.inscripcion_repository.get_by_id(id_inscripcion)
        if not existing_inscripcion:
            raise ValueError(f"Inscripción con ID {id_inscripcion} no encontrada")
        
        # Validar que la inscripción puede ser modificada
        if not existing_inscripcion.puede_ser_modificada():
            raise ValueError("No se puede modificar una inscripción finalizada")
        
        # Aplicar cambios
        if update_dto.estado:
            existing_inscripcion.cambiar_estado(update_dto.estado)
        
        return self.inscripcion_repository.update(id_inscripcion, existing_inscripcion)
    
    def delete(self, id_inscripcion: int) -> bool:
        existing_inscripcion = self.inscripcion_repository.get_by_id(id_inscripcion)
        if not existing_inscripcion:
            raise ValueError(f"Inscripción con ID {id_inscripcion} no encontrada")
        
        # Validar que la inscripción puede ser eliminada
        if not existing_inscripcion.puede_ser_modificada():
            raise ValueError("No se puede eliminar una inscripción finalizada")
        
        return self.inscripcion_repository.delete(id_inscripcion)
    
    def exists_inscripcion_activa(self, id_usuario: int, id_ciclo: int) -> bool:
        return self.inscripcion_repository.exists_inscripcion_activa(id_usuario, id_ciclo)
    
    def finalizar_inscripcion(self, id_inscripcion: int) -> Optional[Inscripcion]:
        """Método específico para finalizar una inscripción"""
        inscripcion = self.inscripcion_repository.get_by_id(id_inscripcion)
        if not inscripcion:
            raise ValueError(f"Inscripción con ID {id_inscripcion} no encontrada")
        
        inscripcion.cambiar_estado(EstadoInscripcionEnum.FINALIZADA)
        return self.inscripcion_repository.update(id_inscripcion, inscripcion)