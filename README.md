# NiASPO - Система управления контрактами

Полнофункциональное веб-приложение для управления контрактами и документооборотом с поддержкой микросервисной архитектуры, Kubernetes и CI/CD.

## 🚀 Быстрый старт

### Локально с Docker Compose

```bash
git clone https://github.com/slobodskoy-a-a/Kursach_NiASPO.git
cd Kursach_NiASPO

docker-compose up -d --build
```

**Доступ:**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🏗️ Архитектура

- **Frontend**: HTML/CSS/JS + Nginx
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Контейнеризация**: Docker
- **Оркестрация**: Kubernetes
- **CI/CD**: GitHub Actions

## 🔑 Основные функции

✅ Создание и управление контрактами  
✅ Изменение статуса контракта  
✅ Удаление контрактов  
✅ Автоматизированные тесты  
✅ CI/CD pipeline с GitHub Actions  
✅ Kubernetes deployment с HPA  
✅ Docker Hub автопуш образов  

## 📚 Эндпоинты API

```
GET    /health              - Проверка здоровья
GET    /contracts/          - Получить все контракты
POST   /contracts/          - Создать контракт
GET    /contracts/{id}      - Получить контракт
PATCH  /contracts/{id}/status - Изменить статус
DELETE /contracts/{id}      - Удалить контракт
```

## ☸️ Kubernetes деплой

```bash
kubectl apply -f k8s/deployment.yaml
kubectl get all -n niaspo
```

## 🐳 Docker Hub

Образы автоматически загружаются на Docker Hub при push в main:
- `slobodskoy/niaspo-backend:latest`
- `slobodskoy/niaspo-frontend:latest`

## 🔄 GitHub Actions

Workflow автоматически:
1. Запускает тесты
2. Собирает Docker образы
3. Загружает на Docker Hub
4. Проверяет безопасность (Trivy scan)

**Требуется настроить секреты:**
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
