from pydantic import BaseModel
from datetime import date
from typing import Optional

# Схема для создания контракта
class ContractCreate(BaseModel):
    title: str
    client: str
    start_date: str
    status: str
    description: Optional[str] = None

# Схема для обновления статуса контракта
class ContractStatusUpdate(BaseModel):
    status: str

# Схема для ответа API (чтение контракта)
class ContractResponse(BaseModel):
    id: int
    title: str
    client: str
    start_date: str
    status: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True  # Заменяет orm_mode = True в Pydantic v2