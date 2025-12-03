#!/bin/bash

echo "🚀 Iniciando Despliegue Automático..."

# 1. Asegurarnos de que estamos en la rama correcta y actualizados
echo "📥 Actualizando repositorio..."
git reset --hard
git pull origin main

# 2. Reconstruir contenedores
echo "🐳 Reconstruyendo contenedores..."
# Asumimos que docker está configurado. Si falla sudo, quitarlo si el user es root/docker group
docker compose down
docker compose up -d --build

# 3. Limpiar imágenes viejas
echo "🧹 Limpiando basura..."
docker image prune -f

echo "✅ ¡Despliegue completado!"