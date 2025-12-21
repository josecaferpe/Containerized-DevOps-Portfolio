#!/bin/bash

# Colores para que se vea bonito en los logs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Iniciando Despliegue Inteligente...${NC}"

# 1. Lógica de Detección de Conflicto
# Comprobamos si existe un contenedor llamado 'uptime-kuma' que NO sea parte de nuestro compose actual
if [ "$(docker ps -q -f name=uptime-kuma)" ]; then
    echo -e "${YELLOW}⚠️  Detectado Uptime Kuma existente (Manual).${NC}"
    echo -e "${YELLOW}🛡️  Se activará el 'Modo Respeto': No se tocará la monitorización existente.${NC}"
    # Dejamos la variable de perfiles VACÍA. Docker Compose ignorará la parte de uptime-kuma.
    export COMPOSE_PROFILES=""
else
    echo -e "${GREEN}✅ El puerto está libre.${NC}"
    echo -e "${GREEN}✨ Se activará el 'Modo Completo': Desplegando Uptime Kuma automático.${NC}"
    # Activamos el perfil 'monitor'. Docker Compose incluirá uptime-kuma.
    export COMPOSE_PROFILES="monitor"
fi

# 2. Reconstrucción y arranque
echo -e "${GREEN}🐳 Aplicando cambios en los contenedores...${NC}"
# Docker Compose leerá la variable COMPOSE_PROFILES automáticamente
docker compose up -d --build --remove-orphans

# 3. Limpieza
echo -e "${GREEN}🧹 Limpiando imágenes antiguas...${NC}"
docker image prune -f

echo -e "${GREEN}✅ ¡Despliegue completado con éxito!${NC}"