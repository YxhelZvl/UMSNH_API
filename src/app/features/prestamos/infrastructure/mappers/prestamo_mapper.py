# src/app/features/prestamos/infrastructure/mappers/prestamo_mapper.py
from src.app.features.prestamos.domain.entities.prestamo import Prestamo
from src.app.features.prestamos.infrastructure.models.prestamo_model import PrestamoDB
from src.app.features.prestamos.domain.value_objects.estado_prestamo import EstadoPrestamo
from src.app.features.prestamos.domain.value_objects.fechas_prestamo import FechasPrestamo

class PrestamoMapper:
    @staticmethod
    def to_domain(prestamo_db: PrestamoDB) -> Prestamo:
        if not prestamo_db:
            return None
            
        fechas = FechasPrestamo(
            fecha_prestamo=prestamo_db.fecha_prestamo,
            fecha_devolucion_esperada=prestamo_db.fecha_devolucion_esperada,
            fecha_devolucion_real=prestamo_db.fecha_devolucion_real
        )
        
        return Prestamo(
            id_prestamo=prestamo_db.id_prestamo,
            id_usuario=prestamo_db.id_usuario,
            id_ejemplar=prestamo_db.id_ejemplar,
            fechas=fechas,
            estado=EstadoPrestamo(valor=prestamo_db.estado)
        )

    @staticmethod
    def to_db(prestamo: Prestamo) -> PrestamoDB:
        if not prestamo:
            return None
            
        return PrestamoDB(
            id_prestamo=prestamo.id_prestamo,
            id_usuario=prestamo.id_usuario,
            id_ejemplar=prestamo.id_ejemplar,
            fecha_prestamo=prestamo.fechas.fecha_prestamo,
            fecha_devolucion_esperada=prestamo.fechas.fecha_devolucion_esperada,
            fecha_devolucion_real=prestamo.fechas.fecha_devolucion_real,
            estado=prestamo.estado.valor.value
        )