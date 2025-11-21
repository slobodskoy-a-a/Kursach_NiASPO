import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base

# Используем in-memory SQLite для тестов (не требует интернета и подключения к БД)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаём таблицы в памяти
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestAPI:
    """Тесты API эндпоинтов"""
    
    def test_read_root(self):
        """Проверка корневого эндпоинта"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert response.json()["message"] == "Contract Management API is running!"

    def test_health_check(self):
        """Проверка health эндпоинта"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestContracts:
    """Тесты CRUD операций контрактов"""
    
    def test_create_contract(self):
        """Тест создания контракта"""
        response = client.post(
            "/contracts/",
            json={
                "title": "Тестовый контракт",
                "client": "ООО Тест",
                "start_date": "2025-01-01",
                "status": "Новый",
                "description": "Тестовое описание"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Тестовый контракт"
        assert data["client"] == "ООО Тест"
        assert data["status"] == "Новый"
        assert "id" in data

    def test_get_contracts_empty(self):
        """Тест получения пустого списка контрактов"""
        response = client.get("/contracts/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_and_get_contracts(self):
        """Тест создания и получения контрактов"""
        # Создаём контракт
        create_response = client.post(
            "/contracts/",
            json={
                "title": "Контракт 1",
                "client": "Клиент 1",
                "start_date": "2025-01-01",
                "status": "Новый"
            }
        )
        assert create_response.status_code == 201
        contract_id = create_response.json()["id"]
        
        # Получаем список контрактов
        response = client.get("/contracts/")
        assert response.status_code == 200
        contracts = response.json()
        assert len(contracts) > 0
        assert any(c["id"] == contract_id for c in contracts)

    def test_get_contract_by_id(self):
        """Тест получения контракта по ID"""
        # Создаём контракт
        create_response = client.post(
            "/contracts/",
            json={
                "title": "Контракт для поиска",
                "client": "Клиент",
                "start_date": "2025-01-01",
                "status": "Новый"
            }
        )
        contract_id = create_response.json()["id"]
        
        # Получаем контракт
        response = client.get(f"/contracts/{contract_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == contract_id
        assert data["title"] == "Контракт для поиска"

    def test_get_nonexistent_contract(self):
        """Тест получения несуществующего контракта"""
        response = client.get("/contracts/99999")
        assert response.status_code == 404

    def test_update_contract_status(self):
        """Тест обновления статуса контракта"""
        # Создаём контракт
        create_response = client.post(
            "/contracts/",
            json={
                "title": "Контракт для обновления",
                "client": "Клиент",
                "start_date": "2025-01-01",
                "status": "Новый"
            }
        )
        contract_id = create_response.json()["id"]
        
        # Обновляем статус
        response = client.patch(
            f"/contracts/{contract_id}/status",
            json={"status": "В работе"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "В работе"

    def test_update_nonexistent_contract_status(self):
        """Тест обновления статуса несуществующего контракта"""
        response = client.patch(
            "/contracts/99999/status",
            json={"status": "В работе"}
        )
        assert response.status_code == 404

    def test_delete_contract(self):
        """Тест удаления контракта"""
        # Создаём контракт
        create_response = client.post(
            "/contracts/",
            json={
                "title": "Контракт для удаления",
                "client": "Клиент",
                "start_date": "2025-01-01",
                "status": "Новый"
            }
        )
        contract_id = create_response.json()["id"]
        
        # Удаляем контракт
        response = client.delete(f"/contracts/{contract_id}")
        assert response.status_code == 200
        
        # Проверяем что контракт удалён
        response = client.get(f"/contracts/{contract_id}")
        assert response.status_code == 404

    def test_delete_nonexistent_contract(self):
        """Тест удаления несуществующего контракта"""
        response = client.delete("/contracts/99999")
        assert response.status_code == 404

