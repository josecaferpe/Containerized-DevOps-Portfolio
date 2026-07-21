#!/bin/bash

# 🛡️ Si cualquier comando falla, el script se detiene aquí mismo
# y el Action se marca en rojo (en vez de seguir como si nada)
set -e

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 Iniciando Despliegue Inteligente...${NC}"

# --- Actualizar repositorio ---
echo -e "${GREEN}📥 Actualizando repositorio...${NC}"

# Guardamos el commit actual ANTES de actualizar, para comparar después
BEFORE=$(git rev-parse HEAD)

if ! git pull origin main; then
    echo -e "${RED}❌ ERROR: git pull falló (probablemente por conflictos con archivos locales).${NC}"
    echo -e "${RED}   Revisa manualmente con: git status${NC}"
    exit 1
fi

AFTER=$(git rev-parse HEAD)

if [ "$BEFORE" == "$AFTER" ]; then
    echo -e "${YELLOW}ℹ️  No había cambios nuevos que desplegar (ya estabas al día).${NC}"
else
    echo -e "${GREEN}✅ Repositorio actualizado: ${BEFORE:0:7} → ${AFTER:0:7}${NC}"
fi

# --- Lógica de Detección de Conflicto ---
if [ "$(docker ps -q -f name=uptime-kuma)" ]; then
    echo -e "${YELLOW}⚠️  Detectado Uptime Kuma existente (Manual).${NC}"
    echo -e "${YELLOW}🛡️  Se activará el 'Modo Respeto': No se tocará la monitorización existente.${NC}"
    export COMPOSE_PROFILES=""
else
    echo -e "${GREEN}✅ El puerto está libre.${NC}"
    echo -e "${GREEN}✨ Se activará el 'Modo Completo': Desplegando Uptime Kuma automático.${NC}"
    export COMPOSE_PROFILES="monitor"
fi

# --- Reconstrucción y arranque ---
echo -e "${GREEN}🐳 Aplicando cambios en los contenedores...${NC}"
docker compose up -d --build --remove-orphans

# --- Limpieza ---
echo -e "${GREEN}🧹 Limpiando imágenes antiguas...${NC}"
docker image prune -f

echo -e "${GREEN}✅ ¡Despliegue completado con éxito!${NC}"
