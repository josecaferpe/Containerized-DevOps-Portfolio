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
Sistema de vigilancia de disponibilidad y estado de servicios.
- **Tech:** Uptime Kuma (Self-hosted).
- **Arquitectura:** Despliegue en VPS (India) para monitorización centralizada de servicios web y contenedores.

---

## Arquitectura del Laboratorio

El sistema opera bajo un modelo de **Nube Híbrida**:

| Rol | Ubicación | Servicios | Hardware |
| :--- | :--- | :--- | :--- |
| **Nube (Pública)** | Bangalore (VPS) | Monitorización (Kuma), Web Server | DigitalOcean Droplet |
| **Edge (Residencial)** | España (Home Lab) | Web Scraping (Wallapop), Media Server | Mini PC (Intel N100) |

## Stack Global

- **Contenedores:** Docker & Docker Compose.
- **Lenguajes:** Python 3.x.
- **Control de Versiones:** Git & GitHub.
- **Notificaciones:** Telegram Bot API (Centralizado).
- **CI/CD:** Despliegues manuales controlados y scripts de automatización.

## Objetivo

El propósito de este repositorio es demostrar competencias en:
1. **Automatización de tareas** repetitivas mediante scripts robustos.
2. **Gestión de contenedores** y orquestación de servicios.
3. **Ingeniería de fiabilidad (SRE)** mediante monitorización proactiva.

---
© 2025 - Jose Carlos | Built with Python & Docker
