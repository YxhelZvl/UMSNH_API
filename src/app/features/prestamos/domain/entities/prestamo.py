# src/app/features/prestamos/domain/entities/prestamo.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from src.app.features.prestamos.domain.value_objects.estado_prestamo import EstadoPrestamo
from src.app.features.prestamos.domain.value_objects.fechas_prestamo import FechasPrestamo

class Prestamo(BaseModel):
    id_prestamo: Optional[int] = None
    id_usuario: int
    id_ejemplar: int
    fechas: FechasPrestamo
    estado: EstadoPrestamo = EstadoPrestamo(valor="activo")

    def devolver(self, fecha_devolucion_real: Optional[datetime] = None):
        """Método de negocio: devolver el préstamo"""
        if self.estado.esta_completado():
            raise ValueError("El préstamo ya ha sido devuelto")
        
        self.fechas.fecha_devolucion_real = fecha_devolucion_real or datetime.now()
        self.estado = EstadoPrestamo(valor="completado")

    def renovar(self, nueva_fecha_devolucion: date):
        """Método de negocio: renovar el préstamo"""
        if not self.estado.esta_activo():
            raise ValueError("Solo se pueden renovar préstamos activos")
        
        if not self.fechas.se_puede_renovar():
            raise ValueError("No se puede renovar un préstamo vencido")
        
        self.fechas.fecha_devolucion_esperada = nueva_fecha_devolucion

    def marcar_como_retrasado(self):
        """Método de negocio: marcar como retrasado"""
        if self.estado.esta_completado():
            raise ValueError("No se puede marcar como retrasado un préstamo completado")
        
        if self.fechas.esta_vencido():
            self.estado = EstadoPrestamo(valor="retrasado")

    def obtener_dias_retraso(self) -> int:
        """Método de negocio: obtener días de retraso"""
        return self.fechas.calcular_dias_retraso()

    def esta_vencido(self) -> bool:
        """Método de negocio: verificar si está vencido"""
        return self.fechas.esta_vencido()

    def se_puede_renovar(self) -> bool:
        """Método de negocio: verificar si se puede renovar"""
        return self.fechas.se_puede_renovar() and self.estado.esta_activo()

    class Config:
        arbitrary_types_allowed = True