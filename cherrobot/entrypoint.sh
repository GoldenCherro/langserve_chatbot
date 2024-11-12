#!/bin/sh

#### Si se quiere usar Ollama, descomentar las siguientes líneas ####

# apt-get update && apt-get install -y netcat-openbsd || apt-get install -y netcat-traditional
# apt-get update && apt-get install -y curl sudo 

# # Espera a que el contenedor de Ollama esté listo
# echo "Esperando a que el contenedor de Ollama esté listo..."
# until nc -z -v -w30 ollama 11434; do
#   echo "Esperando a que el servicio de Ollama esté disponible en el puerto 11434..."
#   sleep 2
# done

# echo "Ollama está listo."

# # Realiza una solicitud POST a la API de Ollama para descargar el modelo
# sh pull_model.sh

# Ejecuta el servidor en segundo plano
langchain serve --port 8000 &
# Ejecuta la aplicación de Streamlit en el puerto 8501
streamlit run app/st_chatbot.py --server.port 8501 --server.address 0.0.0.0
