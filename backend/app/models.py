from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Contract(Base):
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    client = Column(String(255), nullable=False, index=True)
    start_date = Column(String(50))  # Для простоты используем String
    status = Column(String(100), default="черновик")
    description = Column(Text, nullable=True)  # Добавим описание для демонстрации