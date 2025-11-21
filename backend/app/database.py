from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройки для подключения к БД
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@database:5432/contracts_db"

# Создаем движок SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии БД (зависимость)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()