FROM python:3.11-slim

WORKDIR /app

# instalar curl para healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# copiar dependencias primero (optimización)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiar todo el proyecto
COPY . .

EXPOSE 8000

# healthcheck automático de docker
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]