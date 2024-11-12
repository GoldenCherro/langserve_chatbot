#!/bin/sh

# Espera 10 segundos para asegurarse de que Ollama esté listo (ajusta el tiempo si es necesario)
sleep 10

# Realiza una solicitud POST a la API de Ollama para descargar el modelo
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"name":"llama3.2", "stream": false}' \
    http://ollama:11434/api/pull
