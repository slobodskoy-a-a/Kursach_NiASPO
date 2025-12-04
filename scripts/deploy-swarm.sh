#!/bin/bash

# Docker Swarm deployment script for Kursach_NiASPO

set -e

echo "🚀 Docker Swarm Deployment"
echo "=========================="

# Check if Docker Swarm is initialized
if ! docker info | grep -q "Swarm: active"; then
    echo "📌 Initializing Docker Swarm..."
    docker swarm init
else
    echo "✅ Docker Swarm is already active"
fi

# Create network if not exists
echo "🌐 Creating overlay network..."
docker network create -d overlay app-network --opt com.docker.network.driver.mtu=1450 2>/dev/null || true

# Build images
echo "🔨 Building images..."
docker build -t contract_backend:latest ./backend
docker build -t contract_frontend:latest ./frontend

# Create stack from docker-compose.yaml
echo "📦 Deploying stack..."
docker stack deploy -c docker-compose.yaml contracts_stack

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service Status:"
docker service ls

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Access:"
echo "  Frontend: http://localhost"
echo "  API: http://localhost:8000"
echo "  Docs: http://localhost:8000/docs"
echo ""
echo "📝 Useful commands:"
echo "  View services: docker service ls"
echo "  Check logs: docker service logs contracts_stack_backend"
echo "  Scale service: docker service scale contracts_stack_backend=3"
echo "  Remove stack: docker stack rm contracts_stack"
