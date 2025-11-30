FROM python:3.11-slim

WORKDIR /app

# Crear usuario
RUN adduser --disabled-password --gecos '' hunter

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Permisos
RUN chown -R hunter:hunter /app
USER hunter

CMD ["python", "-u", "hunter.py"]