from pydantic import BaseModel
from typing import Any, Optional, List, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')

class GenericResponse(BaseModel, Generic[T]):
    timestamp: str
    status: int
    success: bool
    message: str
    data: Optional[T] = None
    errors: Optional[List[str]] = None
    
    @classmethod
    def create_success(
        cls, 
        message: str, 
        data: Optional[T] = None,
        status: int = 200
    ) -> "GenericResponse[T]":
        return cls(
            timestamp=datetime.now().isoformat(),
            status=status,
            success=True,
            message=message,
            data=data,
            errors=None
        )
    
    @classmethod
    def create_error(
        cls,
        message: str,
        errors: Optional[List[str]] = None,
        status: int = 400
    ) -> "GenericResponse[None]":
        return cls(
            timestamp=datetime.now().isoformat(),
            status=status,
            success=False,
            message=message,
            data=None,
            errors=errors or []
        )

# Schema para paginación
class PaginationMeta(BaseModel):
    page: int
    size: int
    total: int
    pages: int

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    meta: PaginationMeta