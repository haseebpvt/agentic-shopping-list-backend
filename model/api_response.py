from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.v1.generics import GenericModel

T = TypeVar("T")

class ErrorBody(BaseModel):
    code: str
    message: str


class ApiResponse(GenericModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ErrorBody] = None
