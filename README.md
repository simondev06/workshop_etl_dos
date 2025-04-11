# 🎧 Workshop ETL: Datos Musicales
Este proyecto implementa un pipeline ETL (Extract, Transform, Load) utilizando Apache Airflow en Docker para integrar y analizar datos de artistas musicales provenientes de tres fuentes distintas: Spotify, los premios Grammy y Last.fm. El objetivo es consolidar esta información en un modelo dimensional que permita realizar análisis enriquecidos sobre artistas, géneros, popularidad y reconocimientos.

## Estructura del Proyecto:

├── dags/                   # DAG de Airflow para orquestar el pipeline

├── data/

│   ├── raw/                # Datos originales extraídos de las fuentes

│   ├── processed/          # Datos transformados y normalizados

│   └── output/             # Dataset final consolidado y archivos exportados

├── scripts/                # Scripts de etl

├── docker-compose.yaml     # Configuración de Docker para entorno local

├── requirements.txt        # Dependencias del proyecto

└── README.md               # Documentación del proyecto



## Pipeline ETL
El flujo de trabajo está compuesto por las siguientes etapas:

### Extracción: Se obtienen datos de:

Spotify: Información sobre artistas, álbumes, canciones y popularidad.

Premios Grammy: Historial de nominaciones y categorías.

Last.fm: Estadísticas de oyentes, reproducciones y etiquetas asociadas.

### Transformación:

Normalización de nombres de artistas para facilitar la integración.

Agrupación y limpieza de datos por artista.

Cálculo de métricas como popularidad promedio y número de nominaciones.

### Carga:

Fusión de los datasets transformados en un único dataset final.

Almacenamiento del dataset consolidado en formato Parquet.

Exportación del dataset a una base de datos SQLite y a formato CSV.



## Dataset Final
El dataset consolidado contiene información enriquecida por artista, incluyendo:

artist: Nombre original del artista.

album_name: Lista de álbumes únicos asociados.

track_name: Lista de canciones únicas asociadas.

track_genre: Lista de géneros musicales asociados.

popularity: Popularidad promedio del artista en Spotify.

year: Años en los que el artista fue nominado a los Grammy.

category: Categorías de nominación en los Grammy.

nominee: Lista de nominaciones recibidas.

grammy_nominations: Número total de nominaciones a los Grammy.

listeners: Promedio de oyentes en Last.fm.

playcount: Promedio de reproducciones en Last.fm.

tags: Etiquetas asociadas al artista en Last.fm.

Este dataset permite realizar análisis detallados sobre la trayectoria y popularidad de los artistas, así como estudiar la relación entre el reconocimiento en premios y la recepción del público.

## Ejecución del proyecto
Para ejecutar el pipeline ETL:

git clone git@github.com:simondev06/workshop_etl_dos.git
cd workshop_etl_dos
Construir y levantar los servicios con Docker:

docker-compose up --build
Acceder a la interfaz de Airflow:

Abrir http://localhost:8080 en el navegador y ejecutar el DAG etl_pipeline_sws.
