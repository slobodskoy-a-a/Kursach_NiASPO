import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app, get_db
from app.database import Base

# Используем in-memory SQLite для тестов
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Используем правильный синтаксис для TestClient
client = TestClient(app)

class TestContracts:
    def test_read_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Contract Management API is running!"

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_create_contract(self):
        response = client.post(
            "/contracts/",
            json={
                "title": "Test Contract",
                "client": "Test Client",
                "start_date": "2025-01-01",
                "status": "Новый",
                "description": "Test description"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Contract"
        assert data["client"] == "Test Client"
        assert data["status"] == "Новый"

    def test_get_contracts(self):
        # Создаём контракт
        client.post(
            "/contracts/",
            json={
                "title": "Contract 1",
                "client": "Client 1",
                "start_date": "2025-01-01",
                "status": "Новый"
            }
        )
        
        response = client.get("/contracts/")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_contract_by_id(self):
        # Создаём контракт
        create_response = client.post(
            "/contracts/",
            json={
                "title": "Test Contract",
                "client": "Test Client",
                "start_date": "2025-01-01",
                "status": "Новый"
            }
        )
        contract_id = create_response.json()["id"]
        
        # Получаём контракт
        response = client.get(f"/contracts/{contract_id}")
        assert response.status_code == 200
        assert response.json()["id"] == contract_id

    def test_update_contract_status(self):
        # Создаём контракт
        create_response = client.post(
            "/contracts/",
            json={
                "title": "Test Contract",
                "client": "Test Client",
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
        assert response.json()["status"] == "В работе"

    def test_delete_contract(self):
        # Создаём контракт
        create_response = client.post(
            "/contracts/",
            json={
                "title": "Test Contract",
                "client": "Test Client",
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
