# src/app/features/user/domain/entities/user.py
from pydantic import BaseModel
from typing import Optional
from src.app.features.user.domain.value_objects.nombre_usuario import NombreUsuario
from src.app.features.user.domain.value_objects.email import EmailValueObject
from src.app.features.user.domain.value_objects.matricula import MatriculaValueObject

class User(BaseModel):
    id_usuario: Optional[int] = None
    nombre: NombreUsuario
    apellidoP: str
    apellidoM: str
    matricula: MatriculaValueObject
    email: EmailValueObject
    contraseña: str
    id_rol: int
    status: bool = True
    
    def cambiar_nombre(self, nuevo_nombre: str):
        """Método de negocio para cambiar nombre"""
        self.nombre = NombreUsuario(valor=nuevo_nombre)
    
    def cambiar_email(self, nuevo_email: str):
        """Método de negocio para cambiar email"""
        self.email = EmailValueObject(valor=nuevo_email)
    
    def cambiar_matricula(self, nueva_matricula: str):
        """Método de negocio para cambiar matrícula"""
        self.matricula = MatriculaValueObject(valor=nueva_matricula)
    
    def desactivar(self):
        """Método de negocio para desactivar usuario"""
        self.status = False
    
    def activar(self):
        """Método de negocio para activar usuario"""
        self.status = True
    
    def obtener_nombre_completo(self) -> str:
        """Método de negocio: obtiene nombre completo"""
        return f"{self.nombre.valor} {self.apellidoP} {self.apellidoM}"
    
    def es_estudiante(self) -> bool:
        """Método de negocio: verifica si es estudiante"""
        return self.id_rol == 1  # ID del rol Estudiante
    
    def es_maestro(self) -> bool:
        """Método de negocio: verifica si es maestro"""
        return self.id_rol == 2  # ID del rol Maestro
    
    def es_administrativo(self) -> bool:
        """Método de negocio: verifica si es administrativo"""
        return self.id_rol == 3  # ID del rol Administrativo
    
    def es_bibliotecario(self) -> bool:
        """Método de negocio: verifica si es bibliotecario"""
        return self.id_rol == 4  # ID del rol Bibliotecario
    
    class Config:
        arbitrary_types_allowed = True