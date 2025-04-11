import pandas as pd
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

def extract_spotify_data(num_registros=1210):
    input_path_csv = "/opt/airflow/data/raw/spotify/spotify.csv"
    output_path = "/opt/airflow/data/processed/spotify.parquet"

    try:
        # Leer el archivo CSV
        df_spotify = pd.read_csv(input_path_csv)

        # Filtrar canciones por popularidad
        df_spotify = df_spotify.sort_values(by="popularity", ascending=False)

        # ➕ Filtrar solo canciones con un único artista (sin ";")
        df_spotify = df_spotify[df_spotify['artists'].apply(lambda x: isinstance(x, str) and ";" not in x)]

        # Limitar al número deseado de registros
        df_spotify = df_spotify.head(num_registros)

        # Extraer y normalizar artista
        df_spotify['artist_list'] = df_spotify['artists'].apply(lambda x: [x.strip()] if pd.notna(x) else [])
        df_spotify['artist_normalized'] = df_spotify['artist_list'].apply(
            lambda artists: normalize_artist(artists[0]) if artists else ""
        )

        # Guardar como parquet
        df_spotify.to_parquet(output_path, index=False)
        print(f"✅ Spotify guardado en {output_path}")
        print(df_spotify[['artists', 'artist_normalized']])
        return df_spotify

    except Exception as e:
        print(f"❌ Error al extraer Spotify: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        num = int(sys.argv[1])
    except:
        num = 1210
    extract_spotify_data(num)

