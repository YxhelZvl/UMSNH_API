# src/app/features/user/infrastructure/mappers/user_mapper.py
from src.app.features.user.domain.entities.user import User
from src.app.features.user.domain.value_objects.nombre_usuario import NombreUsuario
from src.app.features.user.domain.value_objects.email import EmailValueObject
from src.app.features.user.domain.value_objects.matricula import MatriculaValueObject
from src.app.features.user.infrastructure.models.user_model import UserDB

class UserMapper:
    """Mapper para convertir entre la entidad de dominio User y el modelo de BD UserDB"""

    @staticmethod
    def to_domain(user_db: UserDB) -> User:
        """Convierte UserDB (modelo de BD) a User (entidad de dominio)"""
        if not user_db:
            return None
            
        # Convertir status string a booleano
        status_bool = user_db.status == "activo"
        
        return User(
            id_usuario=user_db.id_usuario,
            nombre=NombreUsuario(valor=user_db.nombre),
            apellidoP=user_db.apellidoP,
            apellidoM=user_db.apellidoM,
            matricula=MatriculaValueObject(valor=user_db.matricula),
            email=EmailValueObject(valor=user_db.email),
            contraseña=user_db.contraseña,
            id_rol=user_db.id_rol,
            status=status_bool
        )

    @staticmethod
    def to_db(user: User) -> UserDB:
        """Convierte User (entidad de dominio) a UserDB (modelo de BD)"""
        if not user:
            return None
            
        # Convertir booleano a string para status
        status_str = "activo" if user.status else "inactivo"
        
        return UserDB(
            id_usuario=user.id_usuario,
            nombre=user.nombre.valor,
            apellidoP=user.apellidoP,
            apellidoM=user.apellidoM,
            matricula=user.matricula.valor,
            email=user.email.valor,
            contraseña=user.contraseña,
            id_rol=user.id_rol,
            status=status_str
        )