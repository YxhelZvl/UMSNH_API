# src/app/features/user/domain/repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.features.user.domain.entities.user import User

class UserRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[User]:
        pass
    
    @abstractmethod
    def get_by_id(self, id_usuario: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_matricula(self, matricula: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_rol(self, id_rol: int) -> List[User]:
        pass
    
    @abstractmethod
    def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    def update(self, id_usuario: int, user: User) -> Optional[User]:
        pass
    
    @abstractmethod
    def delete(self, id_usuario: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def exists_by_matricula(self, matricula: str) -> bool:
        pass