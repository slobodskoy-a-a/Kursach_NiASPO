from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import engine, get_db

# Создаем таблицы в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contract Management API",
    description="API для системы управления контрактами и документооборотом",
    version="1.0.0"
)

# Настройка CORS для взаимодействия с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любых источников (для разработки)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Эндпоинт для проверки работы сервиса
@app.get("/")
def read_root():
    return {"message": "Contract Management API is running!"}

# Эндпоинт для проверки здоровья сервиса
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Эндпоинт для создания контракта
@app.post("/contracts/", response_model=schemas.ContractResponse, status_code=status.HTTP_201_CREATED)
def create_new_contract(contract: schemas.ContractCreate, db: Session = Depends(get_db)):
    """Создать новый контракт"""
    return crud.create_contract(db=db, contract=contract)

# Эндпоинт для получения всех контрактов
@app.get("/contracts/", response_model=List[schemas.ContractResponse])
def read_contracts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех контрактов"""
    contracts = crud.get_contracts(db, skip=skip, limit=limit)
    return contracts

# Эндпоинт для получения контракта по ID
@app.get("/contracts/{contract_id}", response_model=schemas.ContractResponse)
def read_contract(contract_id: int, db: Session = Depends(get_db)):
    """Получить контракт по ID"""
    db_contract = crud.get_contract(db, contract_id=contract_id)
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    return db_contract

# Эндпоинт для удаления контракта
@app.delete("/contracts/{contract_id}")
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    """Удалить контракт по ID"""
    success = crud.delete_contract(db, contract_id=contract_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contract not found")
    return {"message": "Contract deleted successfully"}

# Эндпоинт для обновления статуса контракта
@app.patch("/contracts/{contract_id}/status", response_model=schemas.ContractResponse)
def update_contract_status(contract_id: int, status_update: schemas.ContractStatusUpdate, db: Session = Depends(get_db)):
    """Обновить статус контракта"""
    db_contract = crud.update_contract_status(db, contract_id=contract_id, new_status=status_update.status)
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    return db_contract