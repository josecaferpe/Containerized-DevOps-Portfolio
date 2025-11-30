# 📚 Glosario Técnico del Home Lab

Este documento contiene una referencia rápida de los términos clave de SysAdmin, DevOps y automatización utilizados en el desarrollo y despliegue del SysOps Lab.

## 🐳 Contenedores y Orquestación

| Término | Definición y Contexto |
| :--- | :--- |
| **Docker** | Plataforma que permite empaquetar una aplicación y todas sus dependencias (código, librerías, sistema operativo minimalista) en un **contenedor** portable y aislado. |
| **Contenedor** | Instancia ligera y aislada de un sistema operativo virtualizado donde se ejecuta una aplicación. Es el resultado de ejecutar una **Imagen Docker**. |
| **Imagen Docker** | Plantilla de solo lectura que contiene las instrucciones para construir un contenedor (ej: una imagen base de Python 3.9 con Selenium). |
| **Docker Compose** | Herramienta para definir y ejecutar aplicaciones multi-contenedor. Permite orquestar varios servicios (App, Chrome, Uptime Kuma) en un solo fichero YAML. |
| **Volumen** | Mecanismo que permite a los contenedores acceder a carpetas del sistema operativo anfitrión. Vital para la **persistencia de datos** (ej: `memoria.json`, base de datos de Uptime Kuma). |
| **Headless** | Modo de ejecución de un navegador (como Chrome) **sin interfaz gráfica**. Usado por **Wallapop Hunter** para simular un usuario real sin abrir ventanas visibles. |
| **PUID/PGID** | *User ID / Group ID*. Se usan en Docker para asignar los permisos de los archivos creados por el contenedor a un usuario específico del sistema anfitrión. |

---

## 💻 Arquitectura y Hardware

| Término | Definición y Contexto |
| :--- | :--- |
| **Home Lab** | Entorno de servidores, *networking* y software montado en casa para aprender, experimentar y automatizar tareas. |
| **VPS** | *Virtual Private Server*. Servidor virtualizado alojado en un centro de datos externo (ej: DigitalOcean en India). Se usa para servicios que requieren IP pública constante. |
| **Nube Híbrida** | Arquitectura que combina infraestructuras propias (Home Lab) con servicios de nube pública (VPS). |
| **Puerto** | Número que identifica un servicio concreto en una máquina (ej: el puerto `3001` es el estándar para Uptime Kuma). |

---

## 🤖 Automatización y Desarrollo

| Término | Definición y Contexto |
| :--- | :--- |
| **Web Scraping** | Técnica de extracción de datos de páginas web. Tu **Scrapper Bot** usa Requests, y **Wallapop Hunter** usa Selenium. |
| **Stateful** | Se refiere a una aplicación o sistema que **mantiene el estado** (la memoria) de interacciones previas. **Wallapop Hunter** es *stateful* gracias a `memoria.json`. |
| **CI/CD** | *Continuous Integration / Continuous Deployment*. Prácticas de DevOps para automatizar las pruebas y el despliegue de código (Tus *GitHub Actions* y scripts `deploy.sh`). |
| **Heartbeat (Latido)** | Señal periódica enviada por un servicio para indicar que está vivo. Los bots envían un *latido pasivo* a Uptime Kuma para que lo monitorice. |
| **Requests** | Librería de Python para realizar peticiones HTTP sencillas. Utilizado para el **Scrapper Estático** (BOE/INAP). |
| **Selenium** | Herramienta que automatiza navegadores web reales. Usada por **Wallapop Hunter** para ejecutar JavaScript, simular *scroll* y evadir defensas web. |
| **BeautifulSoup4** | Librería de Python para analizar (parsear) documentos HTML y XML. Se usa para encontrar y extraer los datos importantes de la estructura de la web. |

---

## 🛡️ Buenas Prácticas y Seguridad

| Término | Definición y Contexto |
| :--- | :--- |
| **`.gitignore`** | Archivo que indica a Git qué ficheros e información sensible debe **ignorar** y no subir al repositorio público (ej: `.env`, `memoria.json`). |
| **`.env`** | Archivo de texto plano usado para almacenar **variables de entorno** (claves de API, tokens de Telegram). Es un estándar de seguridad. |
| **YAML** | *YAML Ain't Markup Language*. Formato de serialización de datos, usado comúnmente en ficheros de configuración de Docker Compose. |
