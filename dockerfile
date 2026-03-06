# Imagen base — Python 3.11 liviano
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero requirements para aprovechar el cache de Docker
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY config.py .
COPY src/ ./src/

# Variable de entorno para que Python no genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# El handler que Lambda va a llamar
CMD ["python", "src/lambda_handler.py"]