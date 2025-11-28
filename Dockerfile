FROM python:3.11-slim

# Evita que Python guarde archivos .pyc y fuerza logs inmediatos
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Crear usuario no-root (Seguridad)
RUN adduser --disabled-password --gecos '' sysadmin
USER sysadmin

# Comando por defecto
CMD ["python", "monitor.py"]