#!/bin/sh

apt-get update && apt-get install -y netcat-openbsd || apt-get install -y netcat-traditional
apt-get update && apt-get install -y curl sudo 

# Espera a que el contenedor de Ollama esté listo
echo "Esperando a que el contenedor de Ollama esté listo..."
until nc -z -v -w30 ollama 11434; do
  echo "Esperando a que el servicio de Ollama esté disponible en el puerto 11434..."
  sleep 2
done

echo "Ollama está listo."

# Realiza una solicitud POST a la API de Ollama para descargar el modelo
sh pull_model.sh

# Ejecuta el proceso principal de la aplicación
echo "Iniciando la aplicación..."

exec uvicorn app.server:app --host 0.0.0.0 --port 8000
