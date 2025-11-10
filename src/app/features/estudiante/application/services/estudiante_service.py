# src/app/features/estudiante/application/services/estudiante_service.py
from typing import List, Optional
from src.app.features.estudiante.domain.entities.estudiante import Estudiante
from src.app.features.estudiante.domain.repositories.estudiante_repository import EstudianteRepository
from src.app.features.estudiante.application.dtos import CreateEstudianteDTO, UpdateEstudianteDTO

# Importamos los servicios/repositorios de las dependencias
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.features.carrera.domain.repositories.carrera_repository import CarreraRepository
# Importamos las entidades de User y Carrera para obtener datos completos
from src.app.features.user.domain.entities.user import User as UserEntity
from src.app.features.carrera.domain.entities.carrera import Carrera as CarreraEntity


class EstudianteService:
    def __init__(
        self, 
        estudiante_repository: EstudianteRepository,
        user_repository: UserRepository,
        carrera_repository: CarreraRepository
    ):
        self.estudiante_repository = estudiante_repository
        self.user_repository = user_repository
        self.carrera_repository = carrera_repository
    
    def get_all(self) -> List[Estudiante]:
        return self.estudiante_repository.get_all()
    
    def get_by_id(self, id_estudiante: int) -> Optional[Estudiante]:
        return self.estudiante_repository.get_by_id(id_estudiante)
    
    def get_by_usuario_id(self, id_usuario: int) -> Optional[Estudiante]:
        return self.estudiante_repository.get_by_usuario_id(id_usuario)
    
    def get_by_carrera_id(self, id_carrera: int) -> List[Estudiante]:
        return self.estudiante_repository.get_by_carrera_id(id_carrera)
    
    def create(self, create_dto: CreateEstudianteDTO) -> Estudiante:
        # Validar que el usuario existe
        usuario = self.user_repository.get_by_id(create_dto.id_usuario)
        if not usuario:
            raise ValueError(f"Usuario con ID {create_dto.id_usuario} no encontrado")
        
        # Validar que la carrera existe
        carrera = self.carrera_repository.get_by_id(create_dto.id_carrera)
        if not carrera:
            raise ValueError(f"Carrera con ID {create_dto.id_carrera} no encontrada")
        
        # Validar que no exista ya un estudiante para este usuario
        existing_estudiante = self.estudiante_repository.get_by_usuario_id(create_dto.id_usuario)
        if existing_estudiante:
            raise ValueError(f"Ya existe un estudiante para el usuario con ID {create_dto.id_usuario}")
        
        # Crear la entidad
        estudiante = Estudiante(
            id_estudiante=None,
            id_usuario=create_dto.id_usuario,
            id_carrera=create_dto.id_carrera
        )
        
        return self.estudiante_repository.create(estudiante)
    
    def update(self, id_estudiante: int, update_dto: UpdateEstudianteDTO) -> Optional[Estudiante]:
        # Validar que el estudiante existe
        existing_estudiante = self.estudiante_repository.get_by_id(id_estudiante)
        if not existing_estudiante:
            raise ValueError(f"Estudiante con ID {id_estudiante} no encontrado")
        
        # Si se está actualizando la carrera, validar que existe
        if update_dto.id_carrera is not None:
            carrera = self.carrera_repository.get_by_id(update_dto.id_carrera)
            if not carrera:
                raise ValueError(f"Carrera con ID {update_dto.id_carrera} no encontrada")
            existing_estudiante.id_carrera = update_dto.id_carrera
        
        return self.estudiante_repository.update(id_estudiante, existing_estudiante)
    
    def delete(self, id_estudiante: int) -> bool:
        # Validar que el estudiante existe
        existing_estudiante = self.estudiante_repository.get_by_id(id_estudiante)
        if not existing_estudiante:
            raise ValueError(f"Estudiante con ID {id_estudiante} no encontrado")
        
        return self.estudiante_repository.delete(id_estudiante)
    
    def exists_by_usuario_id(self, id_usuario: int) -> bool:
        return self.estudiante_repository.exists_by_usuario_id(id_usuario)
    
    
    def get_all_with_details(self) -> List[dict]:
        """Obtener todos los estudiantes con datos detallados usando JOIN"""
        return self.estudiante_repository.get_all_with_details()
    
    def get_by_id_with_details(self, id_estudiante: int) -> Optional[dict]:
        """Obtener estudiante por ID con datos detallados usando JOIN"""
        return self.estudiante_repository.get_by_id_with_details(id_estudiante)
    
    def get_by_usuario_id_with_details(self, id_usuario: int) -> Optional[dict]:
        """Obtener estudiante por ID de usuario con datos detallados usando JOIN"""
        return self.estudiante_repository.get_by_usuario_id_with_details(id_usuario)
    
    def get_by_carrera_id_with_details(self, id_carrera: int) -> List[dict]:
        """Obtener estudiantes por ID de carrera con datos detallados usando JOIN"""
        return self.estudiante_repository.get_by_carrera_id_with_details(id_carrera)