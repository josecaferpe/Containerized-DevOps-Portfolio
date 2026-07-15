- **Estado de la Automatización:** 💯 100% FUNCIONAL Y AUTÓNOMA

## 🚦 Estado del Sistema
- **Infraestructura:** VPS en India 🇮🇳
- **Despliegue:** Automático (GitHub Actions) ✅
- **Estado:** 🟢 OPERATIVO

---

# SysOps & DevOps Lab

Bienvenido a mi laboratorio personal de **Ingeniería de Sistemas, Automatización y DevOps**.

Este repositorio centraliza diversas herramientas, bots y servicios desplegados en una arquitectura híbrida (VPS + Home Lab), aplicando prácticas de **Infrastructure as Code (IaC)**, **Containerización** y **Monitorización**.

## Proyectos Activos

### 1. Wallapop Hunter (./wallapop-hunter)
Un sistema complejo de **Web Scraping con Selenium** diseñado para detectar oportunidades de mercado (Cualquier producto) en tiempo real.
- **Tech:** Selenium WebDriver, Chrome Headless, Python, Docker.
- **Highlights:** Evasión de detección, scroll infinito dinámico, modo visual y persistencia de datos JSON.

### 2. Scrapper Bot (./scrapper-bot)
Bot de vigilancia ligero para webs estáticas. Actualmente configurado como **"INAP Sniper"** para monitorizar boletines oficiales (BOE) y convocatorias públicas.
- **Tech:** BeautifulSoup4, Requests, Python.
- **Highlights:** Consumo mínimo de recursos, parsing HTML rápido y alertas críticas.

### 3. Infraestructura & Monitorización (./uptime-kuma)
Sistema de vigilancia de disponibilidad y estado de servicios, desplegado de forma redundante en ambos entornos de la arquitectura híbrida.
- **Tech:** Uptime Kuma (Self-hosted).
- **Arquitectura:** Instancia en VPS (India) para monitorización de servicios públicos/externos, e instancia local en el Home Lab (Mini PC) para supervisión de contenedores y servicios internos de la red doméstica.

### 4. DNS & Reverse Proxy Local (./local-dns)
Servicio de resolución DNS local y proxy inverso para el Home Lab, permitiendo el acceso a todos los paneles de administración (Portainer, Uptime Kuma, etc.) mediante dominios internos personalizados en lugar de IPs y puertos.
- **Tech:** Pi-hole (DNS Server + Ad-Blocking), Nginx Proxy Manager (Reverse Proxy + SSL Termination), Docker.
- **Highlights:** Resolución de dominios `.lan` internos (`portainer.lan`, `uptime.lan`, etc.), bloqueo de publicidad/tracking a nivel de red, gestión centralizada de certificados y enrutamiento HTTP mediante Nginx Proxy Manager.

---

## Arquitectura del Laboratorio

El sistema opera bajo un modelo de **Nube Híbrida**:

| Rol | Ubicación | Servicios | Hardware |
| :--- | :--- | :--- | :--- |
| **Nube (Pública)** | Bangalore (VPS) | Monitorización (Kuma), Flight Searches | DigitalOcean Droplet |
| **Edge (Residencial)** | España (Home Lab) | Monitorización (Kuma), Web Scraper (Tanto Stateful como static), DNS Local (Pi-hole), Reverse Proxy (NPM), Portainer | Mini PC (Intel N100) |

## Stack Global

- **Contenedores:** Docker & Docker Compose.
- **Lenguajes:** Python 3.x.
- **Redes & DNS:** Pi-hole (DNS local + Ad-Blocking), Nginx Proxy Manager (Reverse Proxy).
- **Gestión de Contenedores:** Portainer.
- **Control de Versiones:** Git & GitHub.
- **Notificaciones:** Telegram Bot API (Centralizado).
- **CI/CD:** Despliegues manuales controlados y scripts de automatización.

## Objetivo

El propósito de este repositorio es demostrar competencias en:

1. **Automatización de tareas** repetitivas mediante scripts robustos.
2. **Gestión de contenedores** y orquestación de servicios.
3. **Ingeniería de fiabilidad (SRE)** mediante monitorización proactiva.
4. **Administración de redes** mediante DNS local y proxy inverso para acceso simplificado a servicios internos.

---
© 2025 - Jose Carlos | Built with Python & Docker
