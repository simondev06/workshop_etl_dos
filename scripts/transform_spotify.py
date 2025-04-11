import pandas as pd
import ast
import unicodedata
import re
import sys

def normalize_artist(name):
    if pd.isna(name):
        return ""
    name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("utf-8")
    name = name.lower().strip()
    name = re.sub(r"[^\w\s]", "", name)
    return name

def transform_spotify(modo_prueba=True):
    try:
        suffix = "_sample" if modo_prueba else ""

        # Rutas
        path_base = "/opt/airflow/data/processed"
        input_path = f"{path_base}/spotify{suffix}.parquet"
        output_path = f"{path_base}/spotify_transformed{suffix}.parquet"

        # Leer datos
        df = pd.read_parquet(input_path)

        # Convertir string a lista real si es necesario
        df['artists'] = df['artists'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else [x]
        )

        # Extraer el primer artista y normalizarlo
        df['artist_normalized'] = df['artists'].apply(
            lambda artistas: normalize_artist(artistas[0]) if isinstance(artistas, list) and len(artistas) > 0 else None
        )

        # Guardar archivo transformado
        df.to_parquet(output_path, index=False)

        print(f"{'🧪 (modo prueba)' if modo_prueba else '✅'} Transformación de Spotify completada: {output_path}")
        return df

    except Exception as e:
        print(f"❌ Error durante la transformación de Spotify: {e}")
        return None

if __name__ == "__main__":
    modo_prueba = "--test" in sys.argv
    transform_spotify(modo_prueba)

