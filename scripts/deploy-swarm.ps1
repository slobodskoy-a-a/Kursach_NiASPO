# Docker Swarm deployment script for Kursach_NiASPO (Windows)

Write-Host "Docker Swarm Deployment" -ForegroundColor Green
Write-Host "==========================" -ForegroundColor Green

# Check if Docker Swarm is initialized
$swarmStatus = docker info | Select-String "Swarm: active"
if (-not $swarmStatus) {
    Write-Host "Initializing Docker Swarm..." -ForegroundColor Yellow
    docker swarm init
}
else {
    Write-Host "Docker Swarm is already active" -ForegroundColor Green
}

# Create network if not exists
Write-Host "Creating overlay network..." -ForegroundColor Yellow
docker network create -d overlay app-network --opt com.docker.network.driver.mtu=1450 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Network created or already exists" -ForegroundColor Green
}

# Build images
Write-Host "Building images..." -ForegroundColor Yellow
docker build -t contract_backend:latest ./backend
docker build -t contract_frontend:latest ./frontend

# Create stack from docker-compose.yaml
Write-Host "Deploying stack..." -ForegroundColor Yellow
docker stack deploy -c docker-compose.yaml contracts_stack

# Wait for services to be ready
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service status
Write-Host "Service Status:" -ForegroundColor Cyan
docker service ls

Write-Host ""
Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Access:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost"
Write-Host "  API: http://localhost:8000"
Write-Host "  Docs: http://localhost:8000/docs"
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  View services: docker service ls"
Write-Host "  Check logs: docker service logs contracts_stack_backend"
Write-Host "  Scale service: docker service scale contracts_stack_backend=3"
Write-Host "  Remove stack: docker stack rm contracts_stack"
