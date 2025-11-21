from sqlalchemy.orm import Session
from . import models, schemas

def get_contracts(db: Session, skip: int = 0, limit: int = 100):
    """Получить список контрактов с пагинацией"""
    return db.query(models.Contract).offset(skip).limit(limit).all()

def get_contract(db: Session, contract_id: int):
    """Получить контракт по ID"""
    return db.query(models.Contract).filter(models.Contract.id == contract_id).first()

def create_contract(db: Session, contract: schemas.ContractCreate):
    """Создать новый контракт"""
    db_contract = models.Contract(
        title=contract.title,
        client=contract.client,
        start_date=contract.start_date,
        status=contract.status,
        description=contract.description
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def delete_contract(db: Session, contract_id: int):
    """Удалить контракт по ID"""
    contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if contract:
        db.delete(contract)
        db.commit()
        return True
    return False