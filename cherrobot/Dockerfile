FROM python:3.11-slim

# Optimiza la instalación de paquetes y evita dependencias recomendadas
RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl sudo && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala Poetry sin crear virtualenvs
RUN pip install poetry==1.6.1 && poetry config virtualenvs.create false

# Define el directorio de trabajo
WORKDIR /code

# Copia solo los archivos de dependencias primero y los instala
COPY ./pyproject.toml ./README.md ./poetry.lock* ./
COPY ./package[s] ./packages
COPY ./app ./app
RUN poetry install --no-interaction --no-ansi

# Copia los scripts y da permisos de ejecución
COPY entrypoint.sh pull_model.sh /code/
RUN chmod +x /code/pull_model.sh /code/entrypoint.sh

# Expone el puerto y define el entrypoint y el comando de ejecución
EXPOSE 8000
ENTRYPOINT ["/code/entrypoint.sh"]
CMD ["sh", "-c", "uvicorn app.server:app --host 0.0.0.0 --port 8000"]
