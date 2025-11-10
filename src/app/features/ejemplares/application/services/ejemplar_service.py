# src/app/features/ejemplares/application/services/ejemplar_service.py
from typing import List, Optional
from src.app.features.ejemplares.domain.entities.ejemplar import Ejemplar
from src.app.features.ejemplares.domain.repositories.ejemplar_repository import EjemplarRepository
from src.app.features.ejemplares.application.dtos import CreateEjemplarDTO, UpdateEjemplarDTO
from src.app.features.ejemplares.domain.value_objects.codigo_inventario import CodigoInventario
from src.app.features.ejemplares.domain.value_objects.ubicacion_ejemplar import UbicacionEjemplar
from src.app.features.ejemplares.domain.value_objects.estado_ejemplar import EstadoEjemplar

# Importamos dependencias
from src.app.features.catalogo.domain.repositories.catalogo_repository import CatalogoRepository
from src.app.features.bibliotecas.domain.repositories.biblioteca_repository import BibliotecaRepository
from src.app.features.laboratorios.domain.repositories.laboratorio_repository import LaboratorioRepository

class EjemplarService:
    def __init__(
        self, 
        ejemplar_repository: EjemplarRepository,
        catalogo_repository: CatalogoRepository,
        biblioteca_repository: BibliotecaRepository,
        laboratorio_repository: LaboratorioRepository
    ):
        self.ejemplar_repository = ejemplar_repository
        self.catalogo_repository = catalogo_repository
        self.biblioteca_repository = biblioteca_repository
        self.laboratorio_repository = laboratorio_repository
    
    def get_all(self) -> List[Ejemplar]:
        return self.ejemplar_repository.get_all()
    
    def get_by_id(self, id_ejemplar: int) -> Optional[Ejemplar]:
        return self.ejemplar_repository.get_by_id(id_ejemplar)
    
    def get_by_codigo_inventario(self, codigo_inventario: str) -> Optional[Ejemplar]:
        return self.ejemplar_repository.get_by_codigo_inventario(codigo_inventario)
    
    def get_by_catalogo(self, id_catalogo: int) -> List[Ejemplar]:
        return self.ejemplar_repository.get_by_catalogo(id_catalogo)
    
    def get_by_ubicacion(self, ubicacion: str) -> List[Ejemplar]:
        return self.ejemplar_repository.get_by_ubicacion(ubicacion)
    
    def get_by_estado(self, estado: str) -> List[Ejemplar]:
        return self.ejemplar_repository.get_by_estado(estado)
    
    def get_by_biblioteca(self, id_biblioteca: int) -> List[Ejemplar]:
        return self.ejemplar_repository.get_by_biblioteca(id_biblioteca)
    
    def get_by_laboratorio(self, id_laboratorio: int) -> List[Ejemplar]:
        return self.ejemplar_repository.get_by_laboratorio(id_laboratorio)
    
    def create(self, create_dto: CreateEjemplarDTO) -> Ejemplar:
        # Validar que el código de inventario sea único
        existing_ejemplar = self.ejemplar_repository.get_by_codigo_inventario(create_dto.codigo_inventario)
        if existing_ejemplar:
            raise ValueError(f"Ya existe un ejemplar con el código de inventario: {create_dto.codigo_inventario}")
        
        # Validar que el catálogo existe
        catalogo = self.catalogo_repository.get_by_id(create_dto.id_catalogo)
        if not catalogo:
            raise ValueError(f"Catálogo con ID {create_dto.id_catalogo} no encontrado")
        
        # Validar ubicación y referencias
        ubicacion_vo = UbicacionEjemplar(valor=create_dto.ubicacion)
        
        if ubicacion_vo.es_biblioteca():
            if not create_dto.id_biblioteca:
                raise ValueError("Un ejemplar en biblioteca debe tener id_biblioteca")
            biblioteca = self.biblioteca_repository.get_by_id(create_dto.id_biblioteca)
            if not biblioteca:
                raise ValueError(f"Biblioteca con ID {create_dto.id_biblioteca} no encontrada")
        
        if ubicacion_vo.es_laboratorio():
            if not create_dto.id_laboratorio:
                raise ValueError("Un ejemplar en laboratorio debe tener id_laboratorio")
            laboratorio = self.laboratorio_repository.get_by_id(create_dto.id_laboratorio)
            if not laboratorio:
                raise ValueError(f"Laboratorio con ID {create_dto.id_laboratorio} no encontrado")
        
        # Crear los value objects
        codigo_vo = CodigoInventario(valor=create_dto.codigo_inventario)
        estado_vo = EstadoEjemplar(valor=create_dto.estado)
        
        # Crear la entidad
        ejemplar = Ejemplar(
            id_ejemplar=None,
            id_catalogo=create_dto.id_catalogo,
            codigo_inventario=codigo_vo,
            ubicacion=ubicacion_vo,
            id_laboratorio=create_dto.id_laboratorio,
            id_biblioteca=create_dto.id_biblioteca,
            estado=estado_vo
        )
        
        # Validar consistencia
        ejemplar.validar_consistencia_ubicacion()
        
        return self.ejemplar_repository.create(ejemplar)
    
    def update(self, id_ejemplar: int, update_dto: UpdateEjemplarDTO) -> Optional[Ejemplar]:
        existing_ejemplar = self.ejemplar_repository.get_by_id(id_ejemplar)
        if not existing_ejemplar:
            raise ValueError(f"Ejemplar con ID {id_ejemplar} no encontrado")
        
        # Validar código de inventario único si se está cambiando
        if update_dto.codigo_inventario and update_dto.codigo_inventario != existing_ejemplar.codigo_inventario.valor:
            ejemplar_con_mismo_codigo = self.ejemplar_repository.get_by_codigo_inventario(update_dto.codigo_inventario)
            if ejemplar_con_mismo_codigo:
                raise ValueError(f"Ya existe un ejemplar con el código de inventario: {update_dto.codigo_inventario}")
        
        # Validar catálogo si se está cambiando
        if update_dto.id_catalogo and update_dto.id_catalogo != existing_ejemplar.id_catalogo:
            catalogo = self.catalogo_repository.get_by_id(update_dto.id_catalogo)
            if not catalogo:
                raise ValueError(f"Catálogo con ID {update_dto.id_catalogo} no encontrado")
        
        # Actualizar campos
        if update_dto.id_catalogo is not None:
            existing_ejemplar.id_catalogo = update_dto.id_catalogo
        
        if update_dto.codigo_inventario is not None:
            existing_ejemplar.codigo_inventario = CodigoInventario(valor=update_dto.codigo_inventario)
        
        if update_dto.ubicacion is not None:
            existing_ejemplar.ubicacion = UbicacionEjemplar(valor=update_dto.ubicacion)
        
        if update_dto.id_laboratorio is not None:
            existing_ejemplar.id_laboratorio = update_dto.id_laboratorio
        
        if update_dto.id_biblioteca is not None:
            existing_ejemplar.id_biblioteca = update_dto.id_biblioteca
        
        if update_dto.estado is not None:
            existing_ejemplar.estado = EstadoEjemplar(valor=update_dto.estado)
        
        # Validar consistencia después de los cambios
        existing_ejemplar.validar_consistencia_ubicacion()
        
        return self.ejemplar_repository.update(id_ejemplar, existing_ejemplar)
    
    def delete(self, id_ejemplar: int) -> bool:
        existing_ejemplar = self.ejemplar_repository.get_by_id(id_ejemplar)
        if not existing_ejemplar:
            raise ValueError(f"Ejemplar con ID {id_ejemplar} no encontrado")
        
        return self.ejemplar_repository.delete(id_ejemplar)
    
    def exists_by_codigo_inventario(self, codigo_inventario: str) -> bool:
        return self.ejemplar_repository.exists_by_codigo_inventario(codigo_inventario)

    # Métodos para datos detallados
    def get_all_with_details(self) -> List[dict]:
        return self.ejemplar_repository.get_all_with_details()

    def get_by_id_with_details(self, id_ejemplar: int) -> Optional[dict]:
        return self.ejemplar_repository.get_by_id_with_details(id_ejemplar)

    def get_disponibles_for_prestamo(self) -> List[dict]:
        return self.ejemplar_repository.get_disponibles_for_prestamo()

    # Métodos de negocio específicos
    def marcar_como_prestado(self, id_ejemplar: int) -> Optional[Ejemplar]:
        ejemplar = self.ejemplar_repository.get_by_id(id_ejemplar)
        if not ejemplar:
            raise ValueError(f"Ejemplar con ID {id_ejemplar} no encontrado")
        
        ejemplar.marcar_como_prestado()
        return self.ejemplar_repository.update(id_ejemplar, ejemplar)

    def marcar_como_devuelto(self, id_ejemplar: int) -> Optional[Ejemplar]:
        ejemplar = self.ejemplar_repository.get_by_id(id_ejemplar)
        if not ejemplar:
            raise ValueError(f"Ejemplar con ID {id_ejemplar} no encontrado")
        
        ejemplar.marcar_como_devuelto()
        return self.ejemplar_repository.update(id_ejemplar, ejemplar)