#!/bin/bash
# Скрипт для деплоя в Kubernetes кластер

set -e

echo "🚀 NiASPO - Kubernetes деплой"
echo "=============================="

# Проверить наличие kubectl
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl не установлен"
    exit 1
fi

# Проверить подключение к кластеру
echo "🔍 Проверка подключения к кластеру..."
if ! kubectl cluster-info >/dev/null 2>&1; then
    echo "❌ Нет подключения к Kubernetes кластеру"
    exit 1
fi

CLUSTER_NAME=$(kubectl cluster-info 2>/dev/null | head -1 | awk '{print $NF}')
echo "✅ Подключение установлено к: $CLUSTER_NAME"
echo ""

# Спросить о namespace
read -p "Введите namespace (по умолчанию: niaspo): " NAMESPACE
NAMESPACE=${NAMESPACE:-niaspo}

echo "📝 Используемый namespace: $NAMESPACE"
echo ""

# Применить манифесты
echo "📦 Применение K8s манифестов..."
kubectl apply -f k8s/deployment.yaml

# Ждать развёртывания
echo "⏳ Ожидание развёртывания сервисов..."
kubectl rollout status deployment/backend -n $NAMESPACE --timeout=5m || true
kubectl rollout status deployment/frontend -n $NAMESPACE --timeout=5m || true

echo ""

# Показать статус
echo "📊 Статус Pod'ов:"
kubectl get pods -n $NAMESPACE

echo ""
echo "📊 Статус Сервисов:"
kubectl get svc -n $NAMESPACE

echo ""
echo "📊 Статус HPA:"
kubectl get hpa -n $NAMESPACE

echo ""

# Получить внешний IP
echo "🌐 Адреса доступа:"
FRONTEND_IP=$(kubectl get svc frontend -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "pending")
echo "  Frontend: http://$FRONTEND_IP"
echo "  (Если 'pending', используйте: kubectl port-forward svc/frontend 8080:80 -n $NAMESPACE)"

echo ""
echo "✅ Деплой завершён!"
echo ""
echo "📝 Полезные команды:"
echo "  Логи pod:           kubectl logs -n $NAMESPACE deployment/backend -f"
echo "  Shell в pod:        kubectl exec -it -n $NAMESPACE <pod-name> bash"
echo "  Port-forward:       kubectl port-forward -n $NAMESPACE svc/backend 8000:8000"
echo "  Удалить деплой:     kubectl delete -f k8s/deployment.yaml"
echo "  Масштабирование:    kubectl scale deployment backend --replicas=5 -n $NAMESPACE"
