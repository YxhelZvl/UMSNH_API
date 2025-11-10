# src/app/features/bibliotecas/application/services/biblioteca_service.py
from typing import List, Optional
from src.app.features.bibliotecas.domain.entities.biblioteca import Biblioteca
from src.app.features.bibliotecas.domain.repositories.biblioteca_repository import BibliotecaRepository
from src.app.features.bibliotecas.application.dtos import CreateBibliotecaDTO, UpdateBibliotecaDTO

class BibliotecaService:
    def __init__(self, biblioteca_repository: BibliotecaRepository):
        self.biblioteca_repository = biblioteca_repository
    
    def get_all(self) -> List[Biblioteca]:
        return self.biblioteca_repository.get_all()
    
    def get_by_id(self, id_biblioteca: int) -> Optional[Biblioteca]:
        return self.biblioteca_repository.get_by_id(id_biblioteca)
    
    def get_by_nombre(self, nombre: str) -> Optional[Biblioteca]:
        return self.biblioteca_repository.get_by_nombre(nombre)
    
    def create(self, create_dto: CreateBibliotecaDTO) -> Biblioteca:
        # Validar que no exista una biblioteca con el mismo nombre
        existing_biblioteca = self.biblioteca_repository.get_by_nombre(create_dto.nombre)
        if existing_biblioteca:
            raise ValueError(f"Ya existe una biblioteca con el nombre: {create_dto.nombre}")
        
        biblioteca = Biblioteca(
            id_biblioteca=None,
            nombre=create_dto.nombre,
            ubicacion=create_dto.ubicacion
        )
        
        return self.biblioteca_repository.create(biblioteca)
    
    def update(self, id_biblioteca: int, update_dto: UpdateBibliotecaDTO) -> Optional[Biblioteca]:
        existing_biblioteca = self.biblioteca_repository.get_by_id(id_biblioteca)
        if not existing_biblioteca:
            raise ValueError(f"Biblioteca con ID {id_biblioteca} no encontrada")
        
        # Verificar si se está cambiando el nombre y si ya existe otro con el mismo nombre
        if update_dto.nombre is not None and update_dto.nombre != existing_biblioteca.nombre:
            biblioteca_con_mismo_nombre = self.biblioteca_repository.get_by_nombre(update_dto.nombre)
            if biblioteca_con_mismo_nombre:
                raise ValueError(f"Ya existe una biblioteca con el nombre: {update_dto.nombre}")
        
        # Actualizar campos
        if update_dto.nombre is not None:
            existing_biblioteca.nombre = update_dto.nombre
        if update_dto.ubicacion is not None:
            existing_biblioteca.ubicacion = update_dto.ubicacion
        
        return self.biblioteca_repository.update(id_biblioteca, existing_biblioteca)
    
    def delete(self, id_biblioteca: int) -> bool:
        existing_biblioteca = self.biblioteca_repository.get_by_id(id_biblioteca)
        if not existing_biblioteca:
            raise ValueError(f"Biblioteca con ID {id_biblioteca} no encontrada")
        
        return self.biblioteca_repository.delete(id_biblioteca)
    
    def exists_by_nombre(self, nombre: str) -> bool:
        return self.biblioteca_repository.exists_by_nombre(nombre)