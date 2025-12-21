#!/bin/bash

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Iniciando Despliegue Inteligente...${NC}"

# --- 👇 ESTO ES LO QUE FALTABA 👇 ---
echo -e "${GREEN}📥 Actualizando repositorio...${NC}"
git pull origin main
# ------------------------------------

# 1. Lógica de Detección de Conflicto
if [ "$(docker ps -q -f name=uptime-kuma)" ]; then
    echo -e "${YELLOW}⚠️  Detectado Uptime Kuma existente (Manual).${NC}"
    echo -e "${YELLOW}🛡️  Se activará el 'Modo Respeto': No se tocará la monitorización existente.${NC}"
    export COMPOSE_PROFILES=""
else
    echo -e "${GREEN}✅ El puerto está libre.${NC}"
    echo -e "${GREEN}✨ Se activará el 'Modo Completo': Desplegando Uptime Kuma automático.${NC}"
    export COMPOSE_PROFILES="monitor"
fi

# 2. Reconstrucción y arranque
echo -e "${GREEN}🐳 Aplicando cambios en los contenedores...${NC}"
docker compose up -d --build --remove-orphans

# 3. Limpieza
echo -e "${GREEN}🧹 Limpiando imágenes antiguas...${NC}"
docker image prune -f

echo -e "${GREEN}✅ ¡Despliegue completado con éxito!${NC}"