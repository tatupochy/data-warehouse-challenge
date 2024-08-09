# data-warehouse-challenge
Construcción de un Data Warehouse

# Proyecto ETL con Airflow y Docker

## Descripción

Este proyecto implementa un proceso de extracción, transformación y carga (ETL) utilizando Apache Airflow y Docker. El proceso incluye la carga de datos desde archivos CSV a un Data Warehouse PostgreSQL, con la utilización de DAGs para orquestar las tareas.

## Estructura del Proyecto

- `dags/`: Contiene los archivos de definición de los DAGs de Airflow.
- `config/`: Contiene la configuración de Airflow.
- `data/`: Carpeta para archivos de datos.
- `logs/`: Logs generados por Airflow.
- `plugins/`: Plugins personalizados para Airflow.
- `requirements.txt`: Dependencias de Python para el proyecto.
- `init_db.sh`: Script para inicializar la base de datos.
- `docker-compose.yml`: Configuración de Docker Compose.
- `.env`: Variables de entorno.

## Configuración y Ejecución

1. **Clona el repositorio**:
    git clone git@github.com:tatupochy/data-warehouse-challenge.git
    cd data-warehouse-challenge

2. **Crea las tablas correspondientes para el proyecto**
    sudo docker exec -it data-warehouse-challenge_postgres_1 psql -U airflow -d airflow -f /docker-entrypoint-initdb.d/create_tables.sql

3. **Configura las variables de entorno**
    AIRFLOW_UID=1000
    AIRFLOW_GID=0

    # Airflow
    AIRFLOW_IMAGE_NAME=apache/airflow:2.9.3
    AIRFLOW_UID=50000
    AIRFLOW_PROJ_DIR=.
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__BROKER_URL=redis://:@redis:6379/0
    AIRFLOW__CORE__FERNET_KEY=your_fernet_key
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=true
    AIRFLOW__CORE__LOAD_EXAMPLES=true
    AIRFLOW__API__AUTH_BACKENDS=airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session
    AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK=true
    _PIP_ADDITIONAL_REQUIREMENTS=

    # Postgres
    POSTGRES_USER=airflow
    POSTGRES_PASSWORD=airflow
    POSTGRES_DB=airflow

    # Optional settings
    _AIRFLOW_DB_MIGRATE=true
    _AIRFLOW_WWW_USER_CREATE=true
    _AIRFLOW_WWW_USER_USERNAME=airflow
    _AIRFLOW_WWW_USER_PASSWORD=airflow

    # Dag
    DB_NAME=airflow
    DB_USER=airflow
    DB_PASSWORD=airflow
    DB_HOST=postgres
    DB_PORT=5432

4. **Iniciar los servicios**
    usar el tempalte de ejemplo
    docker-compose up -d