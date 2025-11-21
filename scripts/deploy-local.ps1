# Скрипт для быстрого локального деплоя с Docker Compose на Windows

Write-Host "🚀 NiASPO - Локальный деплой" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# Проверить наличие Docker
try {
    docker --version | Out-Null
    Write-Host "✅ Docker найден" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker не установлен" -ForegroundColor Red
    exit 1
}

# Проверить наличие Docker Compose
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose найден" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose не установлен" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Остановить старые контейнеры
Write-Host "🛑 Остановка старых контейнеров..." -ForegroundColor Yellow
docker-compose down -v 2>$null

# Собрать новые образы
Write-Host "🔨 Сборка Docker образов..." -ForegroundColor Yellow
docker-compose build

# Запустить контейнеры
Write-Host "▶️  Запуск контейнеров..." -ForegroundColor Yellow
docker-compose up -d

# Дождаться готовности БД
Write-Host "⏳ Ожидание готовности базы данных..." -ForegroundColor Yellow
$count = 0
while ($count -lt 30) {
    try {
        docker-compose exec -T database pg_isready -U user 2>$null | Out-Null
        Write-Host "✅ База данных готова" -ForegroundColor Green
        break
    } catch {
        $count++
        Write-Host "  Попытка $count/30..."
        Start-Sleep -Seconds 1
    }
}

Write-Host ""

# Проверить статус
Write-Host "📊 Статус контейнеров:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "✅ Деплой завершён!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Доступ к приложению:" -ForegroundColor Cyan
Write-Host "  Frontend:    http://localhost" -ForegroundColor White
Write-Host "  Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:    http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "📝 Команды:" -ForegroundColor Cyan
Write-Host "  Логи:        docker-compose logs -f" -ForegroundColor White
Write-Host "  Остановка:   docker-compose down" -ForegroundColor White
Write-Host "  Перезагрузка: docker-compose restart" -ForegroundColor White
