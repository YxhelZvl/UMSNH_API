# src/app/features/user/application/services/user_service.py
from typing import List, Optional
from src.app.features.user.domain.entities.user import User
from src.app.features.user.domain.value_objects.nombre_usuario import NombreUsuario
from src.app.features.user.domain.value_objects.email import EmailValueObject
from src.app.features.user.domain.value_objects.matricula import MatriculaValueObject
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.features.user.application.dtos import CreateUserDTO, UpdateUserDTO
from passlib.context import CryptContext

# Configuración para encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all(self) -> List[User]:
        """Obtener todos los usuarios"""
        return self.user_repository.get_all()

    def get_by_id(self, id_usuario: int) -> Optional[User]:
        """Obtener usuario por ID"""
        return self.user_repository.get_by_id(id_usuario)

    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return self.user_repository.get_by_email(email)

    def get_by_matricula(self, matricula: str) -> Optional[User]:
        """Obtener usuario por matrícula"""
        return self.user_repository.get_by_matricula(matricula)

    def get_by_rol(self, id_rol: int) -> List[User]:
        """Obtener usuarios por rol"""
        return self.user_repository.get_by_rol(id_rol)

    def create(self, create_dto: CreateUserDTO) -> User:
        """Crear un nuevo usuario"""
        # Verificar unicidad de email y matrícula
        if self.user_repository.exists_by_email(create_dto.email):
            raise ValueError("El email ya está registrado")

        if self.user_repository.exists_by_matricula(create_dto.matricula):
            raise ValueError("La matrícula ya está registrada")

        # Encriptar contraseña
        contraseña_hash = pwd_context.hash(create_dto.contraseña)

        # Crear Value Objects
        nombre_vo = NombreUsuario(valor=create_dto.nombre)
        email_vo = EmailValueObject(valor=create_dto.email)
        matricula_vo = MatriculaValueObject(valor=create_dto.matricula)

        # Crear entidad de dominio
        user = User(
            id_usuario=None,
            nombre=nombre_vo,
            apellidoP=create_dto.apellidoP,
            apellidoM=create_dto.apellidoM,
            matricula=matricula_vo,
            email=email_vo,
            contraseña=contraseña_hash,
            id_rol=create_dto.id_rol,
            status=True
        )

        # Guardar a través del repositorio
        return self.user_repository.create(user)

    def update(self, id_usuario: int, update_dto: UpdateUserDTO) -> Optional[User]:
        """Actualizar un usuario existente"""
        # Verificar que el usuario existe
        existing_user = self.user_repository.get_by_id(id_usuario)
        if not existing_user:
            raise ValueError(f"Usuario con ID {id_usuario} no encontrado")

        # Si se está cambiando el email, verificar que no exista otro con el mismo email
        if update_dto.email and update_dto.email != existing_user.email.valor:
            if self.user_repository.exists_by_email(update_dto.email):
                raise ValueError("El email ya está registrado")

        # Si se está cambiando la matrícula, verificar que no exista otro con la misma matrícula
        if update_dto.matricula and update_dto.matricula != existing_user.matricula.valor:
            if self.user_repository.exists_by_matricula(update_dto.matricula):
                raise ValueError("La matrícula ya está registrada")

        # Aplicar cambios
        if update_dto.nombre is not None:
            existing_user.cambiar_nombre(update_dto.nombre)

        if update_dto.apellidoP is not None:
            existing_user.apellidoP = update_dto.apellidoP

        if update_dto.apellidoM is not None:
            existing_user.apellidoM = update_dto.apellidoM

        if update_dto.matricula is not None:
            existing_user.cambiar_matricula(update_dto.matricula)

        if update_dto.email is not None:
            existing_user.cambiar_email(update_dto.email)

        if update_dto.contraseña is not None:
            # Encriptar nueva contraseña
            contraseña_hash = pwd_context.hash(update_dto.contraseña)
            existing_user.contraseña = contraseña_hash

        if update_dto.id_rol is not None:
            existing_user.id_rol = update_dto.id_rol

        if update_dto.status is not None:
            if update_dto.status:
                existing_user.activar()
            else:
                existing_user.desactivar()

        # Actualizar a través del repositorio
        return self.user_repository.update(id_usuario, existing_user)

    def delete(self, id_usuario: int) -> bool:
        """Eliminar un usuario (lógico: desactivar)"""
        user = self.user_repository.get_by_id(id_usuario)
        if not user:
            raise ValueError(f"Usuario con ID {id_usuario} no encontrado")

        # Desactivar usuario
        user.desactivar()
        return self.user_repository.update(id_usuario, user) is not None

    def authenticate(self, email: str, contraseña: str) -> Optional[User]:
        """Autenticar usuario por email y contraseña"""
        user = self.user_repository.get_by_email(email)
        if user and pwd_context.verify(contraseña, user.contraseña):
            return user
        return None
    
    
    def get_all_users_with_details(self) -> List[dict]:
        """Obtener todos los usuarios con detalles adicionales"""
        return self.user_repository.get_all_users_with_details()