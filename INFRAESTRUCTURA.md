# Infraestructura — SysOps & DevOps Lab

Documento de referencia rápida con la información de red de todos los servicios, en ambos entornos de la arquitectura híbrida.

> ⚠️ Este archivo puede contener nombres de dominio y estructura interna. No incluir contraseñas ni tokens — esos van en `.env`, que nunca se sube al repositorio.

---

## 🏠 Entorno Local (Mac — Home Lab)

**DNS local:** Pi-hole (`local-dns-pihole`) — todos los dominios `.lan` resuelven a `127.0.0.1`
**Reverse Proxy:** Nginx Proxy Manager (`local-proxy`) — admin en `http://localhost:81`

| Servicio | Contenedor | Imagen | Dominio (.lan) | Acceso directo (sin DNS) | Puerto interno | Puerto host | Alias de red |
|---|---|---|---|---|---|---|---|
| Pi-hole | `local-dns-pihole` | `pihole/pihole:latest` | `pihole.lan` | — (sin puerto web mapeado al host) | 80 (web) / 53 (DNS) | 53:53 (tcp/udp) | `pihole`, `local-dns-pihole` |
| Portainer | `local-portainer` | `portainer/portainer-ce:latest` | `portainer.lan` | `http://localhost:9002` | 9000 | 9002:9000 | `portainer`, `local-portainer` |
| Uptime Kuma | `local-uptime-kuma` | `louislam/uptime-kuma:1` | `uptime.lan` | `http://localhost:3001` | 3001 | 3001:3001 | `uptime-kuma`, `local-uptime-kuma` |
| Nginx Proxy Manager | `local-proxy` | `jc21/nginx-proxy-manager:latest` | `proxy.lan` | `http://localhost:81` (admin) | 80 / 81 (admin) | 80:80, 81:81 | `proxy`, `local-proxy` |
| Selenium (Chromium) | `local-selenium` | `seleniarm/standalone-chromium:latest` | — | `http://localhost:7900` (noVNC) | 4444, 7900 | 4444:4444, 7900:7900 | `local-selenium` |
| Scraper Bot (INAP Sniper) | `local-scraper-bot` | build local | — | — (sin panel web) | (sin puerto expuesto) | — | `local-scraper-bot` |
| Wallapop Hunter | `local-wallapop-hunter` | build local | — | — (sin panel web) | (sin puerto expuesto) | — | `local-wallapop-hunter` |

**Red Docker:** `containerized-devops-portfolio_default`

---

## 🌐 Entorno VPS (India — DigitalOcean, Bangalore)

**IP pública del VPS:** `128.199.29.231`
**Dominio público:** DuckDNS — `jose-sysops-lab.duckdns.org` (wildcard, cualquier subdominio resuelve a la misma IP)
**DNS local del VPS:** Pi-hole (`local-dns-pihole`) — puerto 53 propio del sistema, liberado de `systemd-resolved`
**Reverse Proxy:** Nginx Proxy Manager (`local-proxy`) — admin en `http://128.199.29.231:81`
**SSL:** Let's Encrypt (automático vía NPM) en todos los subdominios públicos

| Servicio | Contenedor | Imagen | Dominio público | Acceso directo (sin DNS, por IP) | Puerto interno | Puerto host | Alias de red |
|---|---|---|---|---|---|---|---|
| Pi-hole | `local-dns-pihole` | `pihole/pihole:latest` | `pihole.jose-sysops-lab.duckdns.org` | — (sin puerto web mapeado al host) | 80 (web) / 53 (DNS) | 53:53 (tcp/udp) | `pihole`, `local-dns-pihole` |
| Portainer | `local-portainer` | `portainer/portainer-ce:latest` | `portainer.jose-sysops-lab.duckdns.org` | `http://128.199.29.231:9002` | 9000 | 9002:9000 | `portainer`, `local-portainer` |
| Uptime Kuma | `local-uptime-kuma` | `louislam/uptime-kuma:1` | `uptime.jose-sysops-lab.duckdns.org` | `http://128.199.29.231:3001` | 3001 | 3001:3001 | `uptime-kuma`, `local-uptime-kuma` |
| Nginx Proxy Manager | `local-proxy` | `jc21/nginx-proxy-manager:latest` | — (acceso admin por IP:81) | `http://128.199.29.231:81` (admin) | 80 / 81 (admin) / 443 | 80:80, 81:81, 443:443 | `proxy`, `local-proxy` |
| Selenium (Chromium) | `local-selenium` | `seleniarm/standalone-chromium:latest` | — | `http://128.199.29.231:7900` (noVNC) | 4444, 7900, 5900 | 4444:4444, 7900:7900 | `local-selenium` |
| Scraper Bot (INAP Sniper) | `local-scraper-bot` | build (`sysops-lab-scraper-bot`) | — | — (sin panel web) | (sin puerto expuesto) | — | `local-scraper-bot` — monitorizado en Kuma vía socket Docker |
| Wallapop Hunter | `local-wallapop-hunter` | build (`sysops-lab-wallapop-hunter`) | — | — (sin panel web) | (sin puerto expuesto) | — | `local-wallapop-hunter` |

**Red Docker:** `sysops-lab_default`

---

## 🆘 Nota sobre acceso de emergencia a Pi-hole

Pi-hole no tiene su puerto web (80) publicado al host en ninguno de los dos entornos — solo es accesible a través de NPM. Si el DNS falla y necesitas entrar a Pi-hole sin depender de él:
- **Local:** añade temporalmente `127.0.0.1 pihole.lan` a `/etc/hosts` (o publica el puerto 80 del contenedor manualmente con `docker run`/editando el compose)
- **India:** análogo, usando la IP pública `128.199.29.231`

---

## 🔑 Notas de configuración

- **Uptime Kuma en India** tiene montado `/var/run/docker.sock` para poder monitorizar contenedores mediante el tipo de monitor "Docker Container". Portainer también lo tiene (necesario para su función principal).
- **Contraseña de Pi-hole:** variable `PIHOLE_FTL_PASSWORD` en `.env` (nunca en el repo), configurada en ambos entornos.
- **`.gitignore`** excluye los datos reales de Pi-hole y NPM (`etc-pihole/`, `etc-dnsmasq.d/`, `proxy-data/`, `proxy-letsencrypt/`) y logs de los bots (`scraper-bot/logs/`, `scraper-bot/registros/`) — estos archivos existen en disco en cada entorno pero no se sincronizan vía Git.
- **Flujo de despliegue:** Local es la única fuente que hace `git push`. El VPS (India) solo recibe `git pull` automático vía GitHub Actions (`.github/workflows/deploy.yml` → `scripts/deploy.sh`). India nunca debe tener commits propios sin sincronizar — si el índice de Git se desalinea, usar `git reset --hard origin/main` para realinearlo sin perder datos en disco.

---

*Última actualización: Julio 2026*
