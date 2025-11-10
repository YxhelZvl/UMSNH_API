# src/app/features/catalogo/application/services/catalogo_service.py
from typing import List, Optional
from src.app.features.catalogo.domain.entities.catalogo import Catalogo
from src.app.features.catalogo.domain.repositories.catalogo_repository import CatalogoRepository
from src.app.features.catalogo.application.dtos import CreateCatalogoDTO, UpdateCatalogoDTO
from src.app.features.catalogo.domain.value_objects.tipo_item import TipoItem
from src.app.features.catalogo.domain.value_objects.nombre_item import NombreItem
from src.app.features.catalogo.domain.value_objects.isbn import ISBN

class CatalogoService:
    def __init__(self, catalogo_repository: CatalogoRepository):
        self.catalogo_repository = catalogo_repository
    
    def get_all(self) -> List[Catalogo]:
        return self.catalogo_repository.get_all()
    
    def get_by_id(self, id_catalogo: int) -> Optional[Catalogo]:
        return self.catalogo_repository.get_by_id(id_catalogo)
    
    def get_by_nombre(self, nombre: str) -> Optional[Catalogo]:
        return self.catalogo_repository.get_by_nombre(nombre)
    
    def get_by_tipo(self, tipo: str) -> List[Catalogo]:
        return self.catalogo_repository.get_by_tipo(tipo)
    
    def get_by_autor(self, autor: str) -> List[Catalogo]:
        return self.catalogo_repository.get_by_autor(autor)
    
    def get_by_isbn(self, isbn: str) -> Optional[Catalogo]:
        return self.catalogo_repository.get_by_isbn(isbn)
    
    def create(self, create_dto: CreateCatalogoDTO) -> Catalogo:
        # Validar que no exista un item con el mismo nombre
        existing_catalogo = self.catalogo_repository.get_by_nombre(create_dto.nombre)
        if existing_catalogo:
            raise ValueError(f"Ya existe un item en el catálogo con el nombre: {create_dto.nombre}")
        
        # Crear los value objects
        tipo_vo = TipoItem(valor=create_dto.tipo)
        nombre_vo = NombreItem(valor=create_dto.nombre)
        
        # Validaciones de negocio según el tipo
        if tipo_vo.es_libro():
            # Para libros: autor es requerido, ISBN opcional pero debe ser válido si se proporciona
            if not create_dto.autor:
                raise ValueError("Los libros deben tener un autor")
            
            # Validar ISBN único si se proporciona
            if create_dto.isbn:
                existing_isbn = self.catalogo_repository.get_by_isbn(create_dto.isbn)
                if existing_isbn:
                    raise ValueError(f"Ya existe un libro con el ISBN: {create_dto.isbn}")
                isbn_vo = ISBN(valor=create_dto.isbn)
            else:
                isbn_vo = None
        else:
            # Para herramientas y equipos: no deben tener autor ni ISBN
            if create_dto.autor:
                raise ValueError("Solo los libros pueden tener autor")
            if create_dto.isbn:
                raise ValueError("Solo los libros pueden tener ISBN")
            isbn_vo = None
            # Forzar autor a None para herramientas y equipos
            create_dto.autor = None
        
        # Crear la entidad
        catalogo = Catalogo(
            id_catalogo=None,
            tipo=tipo_vo,
            nombre=nombre_vo,
            autor=create_dto.autor,
            isbn=isbn_vo,
            descripcion=create_dto.descripcion
        )
        
        return self.catalogo_repository.create(catalogo)
    
    def update(self, id_catalogo: int, update_dto: UpdateCatalogoDTO) -> Optional[Catalogo]:
        existing_catalogo = self.catalogo_repository.get_by_id(id_catalogo)
        if not existing_catalogo:
            raise ValueError(f"Item del catálogo con ID {id_catalogo} no encontrado")
        
        # Verificar nombre único
        if update_dto.nombre is not None and update_dto.nombre != existing_catalogo.nombre.valor:
            catalogo_con_mismo_nombre = self.catalogo_repository.get_by_nombre(update_dto.nombre)
            if catalogo_con_mismo_nombre:
                raise ValueError(f"Ya existe un item en el catálogo con el nombre: {update_dto.nombre}")
        
        # Determinar el tipo final (si se actualiza o se mantiene el existente)
        tipo_final = update_dto.tipo if update_dto.tipo is not None else existing_catalogo.tipo.valor.value
        tipo_vo_final = TipoItem(valor=tipo_final)
        
        # Validaciones de ISBN según el tipo final
        if tipo_vo_final.es_libro():
            # Para libros: validar ISBN único si se está actualizando
            if update_dto.isbn is not None and update_dto.isbn != (existing_catalogo.isbn.valor if existing_catalogo.isbn else None):
                catalogo_con_mismo_isbn = self.catalogo_repository.get_by_isbn(update_dto.isbn)
                if catalogo_con_mismo_isbn:
                    raise ValueError(f"Ya existe un libro con el ISBN: {update_dto.isbn}")
        else:
            # Para herramientas y equipos: no deben tener ISBN
            if update_dto.isbn is not None:
                raise ValueError("Solo los libros pueden tener ISBN")
            # Si se cambia de libro a herramienta/equipo, remover ISBN
            if existing_catalogo.es_libro() and update_dto.tipo is not None:
                update_dto.isbn = None
        
        # Actualizar campos
        if update_dto.tipo is not None:
            existing_catalogo.tipo = TipoItem(valor=update_dto.tipo)
        
        if update_dto.nombre is not None:
            existing_catalogo.nombre = NombreItem(valor=update_dto.nombre)
        
        if update_dto.autor is not None:
            # Solo permitir autor para libros
            if not tipo_vo_final.es_libro():
                raise ValueError("Solo los libros pueden tener autor")
            existing_catalogo.autor = update_dto.autor
        
        if update_dto.isbn is not None:
            # Solo permitir ISBN para libros
            if not tipo_vo_final.es_libro():
                raise ValueError("Solo los libros pueden tener ISBN")
            existing_catalogo.isbn = ISBN(valor=update_dto.isbn) if update_dto.isbn else None
        
        if update_dto.descripcion is not None:
            existing_catalogo.descripcion = update_dto.descripcion
        
        # Validaciones finales de negocio
        if existing_catalogo.es_libro():
            if not existing_catalogo.autor:
                raise ValueError("Los libros deben tener un autor")
        else:
            # Asegurar que herramientas y equipos no tengan autor ni ISBN
            existing_catalogo.autor = None
            existing_catalogo.isbn = None
        
        return self.catalogo_repository.update(id_catalogo, existing_catalogo)
    
    def delete(self, id_catalogo: int) -> bool:
        existing_catalogo = self.catalogo_repository.get_by_id(id_catalogo)
        if not existing_catalogo:
            raise ValueError(f"Item del catálogo con ID {id_catalogo} no encontrado")
        
        return self.catalogo_repository.delete(id_catalogo)
    
    def exists_by_nombre(self, nombre: str) -> bool:
        return self.catalogo_repository.exists_by_nombre(nombre)
    
    def exists_by_isbn(self, isbn: str) -> bool:
        return self.catalogo_repository.exists_by_isbn(isbn)

    # Métodos para tipos específicos
    def get_libros(self) -> List[Catalogo]:
        return self.catalogo_repository.get_libros()

    def get_herramientas(self) -> List[Catalogo]:
        return self.catalogo_repository.get_herramientas()

    def get_equipos(self) -> List[Catalogo]:
        return self.catalogo_repository.get_equipos()