# src/app/features/prestamos/application/services/prestamo_service.py
from typing import List, Optional
from datetime import datetime, date, timedelta
from src.app.features.prestamos.domain.entities.prestamo import Prestamo
from src.app.features.prestamos.domain.repositories.prestamo_repository import PrestamoRepository
from src.app.features.prestamos.application.dtos import CreatePrestamoDTO, UpdatePrestamoDTO, DevolverPrestamoDTO, RenovarPrestamoDTO
from src.app.features.prestamos.domain.value_objects.estado_prestamo import EstadoPrestamo
from src.app.features.prestamos.domain.value_objects.fechas_prestamo import FechasPrestamo

# Importamos los servicios/repositorios de las dependencias
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.features.ejemplares.domain.repositories.ejemplar_repository import EjemplarRepository

class PrestamoService:
    def __init__(
        self, 
        prestamo_repository: PrestamoRepository,
        user_repository: UserRepository,
        ejemplar_repository: EjemplarRepository
    ):
        self.prestamo_repository = prestamo_repository
        self.user_repository = user_repository
        self.ejemplar_repository = ejemplar_repository
    
    def get_all(self) -> List[Prestamo]:
        return self.prestamo_repository.get_all()
    
    def get_by_id(self, id_prestamo: int) -> Optional[Prestamo]:
        return self.prestamo_repository.get_by_id(id_prestamo)
    
    def get_by_usuario(self, id_usuario: int) -> List[Prestamo]:
        return self.prestamo_repository.get_by_usuario(id_usuario)
    
    def get_by_ejemplar(self, id_ejemplar: int) -> List[Prestamo]:
        return self.prestamo_repository.get_by_ejemplar(id_ejemplar)
    
    def get_by_estado(self, estado: str) -> List[Prestamo]:
        return self.prestamo_repository.get_by_estado(estado)
    
    def get_prestamos_activos(self) -> List[Prestamo]:
        return self.prestamo_repository.get_prestamos_activos()
    
    def get_prestamos_retrasados(self) -> List[Prestamo]:
        return self.prestamo_repository.get_prestamos_retrasados()
    
    def get_prestamos_por_vencer(self, dias: int = 3) -> List[Prestamo]:
        return self.prestamo_repository.get_prestamos_por_vencer(dias)
    
    def create(self, create_dto: CreatePrestamoDTO) -> Prestamo:
        # Validar que el usuario existe
        usuario = self.user_repository.get_by_id(create_dto.id_usuario)
        if not usuario:
            raise ValueError(f"Usuario con ID {create_dto.id_usuario} no encontrado")
        
        # Validar que el ejemplar existe
        ejemplar = self.ejemplar_repository.get_by_id(create_dto.id_ejemplar)
        if not ejemplar:
            raise ValueError(f"Ejemplar con ID {create_dto.id_ejemplar} no encontrado")
        
        # Validar que el ejemplar esté disponible
        if not ejemplar.estado.esta_disponible():
            raise ValueError(f"El ejemplar con ID {create_dto.id_ejemplar} no está disponible para préstamo")
        
        # Validar que el usuario no tenga préstamos activos del mismo ejemplar
        prestamos_activos_usuario = self.prestamo_repository.get_prestamos_activos()
        for prestamo in prestamos_activos_usuario:
            if prestamo.id_usuario == create_dto.id_usuario and prestamo.id_ejemplar == create_dto.id_ejemplar:
                raise ValueError(f"El usuario ya tiene un préstamo activo para este ejemplar")
        
        # Crear los value objects
        fechas_vo = FechasPrestamo(
            fecha_devolucion_esperada=create_dto.fecha_devolucion_esperada
        )
        estado_vo = EstadoPrestamo(valor=create_dto.estado)
        
        # Crear la entidad
        prestamo = Prestamo(
            id_prestamo=None,
            id_usuario=create_dto.id_usuario,
            id_ejemplar=create_dto.id_ejemplar,
            fechas=fechas_vo,
            estado=estado_vo
        )
        
        # Marcar el ejemplar como prestado
        ejemplar.marcar_como_prestado()
        self.ejemplar_repository.update(ejemplar.id_ejemplar, ejemplar)
        
        return self.prestamo_repository.create(prestamo)
    
    def update(self, id_prestamo: int, update_dto: UpdatePrestamoDTO) -> Optional[Prestamo]:
        existing_prestamo = self.prestamo_repository.get_by_id(id_prestamo)
        if not existing_prestamo:
            raise ValueError(f"Préstamo con ID {id_prestamo} no encontrado")
        
        # Validar usuario si se está cambiando
        if update_dto.id_usuario and update_dto.id_usuario != existing_prestamo.id_usuario:
            usuario = self.user_repository.get_by_id(update_dto.id_usuario)
            if not usuario:
                raise ValueError(f"Usuario con ID {update_dto.id_usuario} no encontrado")
        
        # Validar ejemplar si se está cambiando
        if update_dto.id_ejemplar and update_dto.id_ejemplar != existing_prestamo.id_ejemplar:
            ejemplar = self.ejemplar_repository.get_by_id(update_dto.id_ejemplar)
            if not ejemplar:
                raise ValueError(f"Ejemplar con ID {update_dto.id_ejemplar} no encontrado")
        
        # Actualizar campos
        if update_dto.id_usuario is not None:
            existing_prestamo.id_usuario = update_dto.id_usuario
        
        if update_dto.id_ejemplar is not None:
            existing_prestamo.id_ejemplar = update_dto.id_ejemplar
        
        if update_dto.fecha_devolucion_esperada is not None:
            existing_prestamo.fechas.fecha_devolucion_esperada = update_dto.fecha_devolucion_esperada
        
        if update_dto.estado is not None:
            existing_prestamo.estado = EstadoPrestamo(valor=update_dto.estado)
        
        return self.prestamo_repository.update(id_prestamo, existing_prestamo)
    
    def delete(self, id_prestamo: int) -> bool:
        existing_prestamo = self.prestamo_repository.get_by_id(id_prestamo)
        if not existing_prestamo:
            raise ValueError(f"Préstamo con ID {id_prestamo} no encontrado")
        
        # Si el préstamo está activo, marcar el ejemplar como disponible
        if existing_prestamo.estado.esta_activo():
            ejemplar = self.ejemplar_repository.get_by_id(existing_prestamo.id_ejemplar)
            if ejemplar:
                ejemplar.marcar_como_devuelto()
                self.ejemplar_repository.update(ejemplar.id_ejemplar, ejemplar)
        
        return self.prestamo_repository.delete(id_prestamo)

    # Métodos para datos detallados
    def get_all_with_details(self) -> List[dict]:
        return self.prestamo_repository.get_all_with_details()

    def get_by_id_with_details(self, id_prestamo: int) -> Optional[dict]:
        return self.prestamo_repository.get_by_id_with_details(id_prestamo)

    def get_by_usuario_with_details(self, id_usuario: int) -> List[dict]:
        return self.prestamo_repository.get_by_usuario_with_details(id_usuario)

    def get_prestamos_activos_with_details(self) -> List[dict]:
        return self.prestamo_repository.get_prestamos_activos_with_details()

    # Métodos de negocio específicos
    def devolver(self, id_prestamo: int, devolver_dto: DevolverPrestamoDTO) -> Optional[Prestamo]:
        prestamo = self.prestamo_repository.get_by_id(id_prestamo)
        if not prestamo:
            raise ValueError(f"Préstamo con ID {id_prestamo} no encontrado")
        
        # Convertir la fecha de devolución a datetime si es date
        fecha_devolucion_real = devolver_dto.fecha_devolucion_real
        if fecha_devolucion_real and isinstance(fecha_devolucion_real, date):
            fecha_devolucion_real = datetime.combine(fecha_devolucion_real, datetime.now().time())
        
        prestamo.devolver(fecha_devolucion_real)
        
        # Marcar el ejemplar como disponible
        ejemplar = self.ejemplar_repository.get_by_id(prestamo.id_ejemplar)
        if ejemplar:
            ejemplar.marcar_como_devuelto()
            self.ejemplar_repository.update(ejemplar.id_ejemplar, ejemplar)
        
        return self.prestamo_repository.update(id_prestamo, prestamo)

    def renovar(self, id_prestamo: int, renovar_dto: RenovarPrestamoDTO) -> Optional[Prestamo]:
        prestamo = self.prestamo_repository.get_by_id(id_prestamo)
        if not prestamo:
            raise ValueError(f"Préstamo con ID {id_prestamo} no encontrado")
        
        prestamo.renovar(renovar_dto.nueva_fecha_devolucion)
        
        return self.prestamo_repository.update(id_prestamo, prestamo)

    def marcar_retrasados(self):
        """Método para marcar automáticamente los préstamos retrasados"""
        prestamos_activos = self.prestamo_repository.get_prestamos_activos()
        
        for prestamo in prestamos_activos:
            if prestamo.esta_vencido():
                prestamo.marcar_como_retrasado()
                self.prestamo_repository.update(prestamo.id_prestamo, prestamo)