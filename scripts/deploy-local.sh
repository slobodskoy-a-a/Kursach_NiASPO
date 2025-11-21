#!/bin/bash
# Скрипт для быстрого локального деплоя с Docker Compose

set -e

echo "🚀 NiASPO - Локальный деплой"
echo "=============================="

# Проверить наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен"
    exit 1
fi

# Проверить наличие Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен"
    exit 1
fi

echo "✅ Docker найден"

# Остановить старые контейнеры
echo "🛑 Остановка старых контейнеров..."
docker-compose down -v 2>/dev/null || true

# Очистить неиспользуемые образы
echo "🧹 Очистка Docker образов..."
docker system prune -f || true

# Собрать новые образы
echo "🔨 Сборка Docker образов..."
docker-compose build

# Запустить контейнеры
echo "▶️  Запуск контейнеров..."
docker-compose up -d

# Дождаться готовности БД
echo "⏳ Ожидание готовности базы данных..."
for i in {1..30}; do
    if docker-compose exec -T database pg_isready -U user >/dev/null 2>&1; then
        echo "✅ База данных готова"
        break
    fi
    echo "  Попытка $i/30..."
    sleep 1
done

# Проверить статус
echo ""
echo "📊 Статус контейнеров:"
docker-compose ps

echo ""
echo "✅ Деплой завершён!"
echo ""
echo "🌐 Доступ к приложению:"
echo "  Frontend:    http://localhost"
echo "  Backend API: http://localhost:8000"
echo "  API Docs:    http://localhost:8000/docs"
echo ""
echo "📝 Команды:"
echo "  Логи:        docker-compose logs -f"
echo "  Остановка:   docker-compose down"
echo "  Перезагрузка: docker-compose restart"
