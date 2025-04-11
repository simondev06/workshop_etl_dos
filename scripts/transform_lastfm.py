import pandas as pd
import unicodedata
import re
import sys

def normalize_artist(name):
    if pd.isna(name):
        return ""
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    name = name.lower().strip()
    name = re.sub(r"[^\w\s]", "", name)
    return name

def transform_lastfm(modo_prueba=True):
    input_path = "/opt/airflow/data/processed/lastfm.parquet"

    try:
        df = pd.read_parquet(input_path)

        # Normalización y limpieza
        df['artist_normalized'] = df['artist'].apply(normalize_artist)

        # Asegurarse de que los campos vengan como string antes de convertirlos
        df['listeners'] = pd.to_numeric(df['listeners'].astype(str), errors='coerce')
        df['playcount'] = pd.to_numeric(df['playcount'].astype(str), errors='coerce')

        df = df.dropna(subset=['listeners', 'playcount', 'artist_normalized'])
        df = df.drop_duplicates(subset=['artist_normalized'])

        columnas = ['artist', 'artist_normalized', 'listeners', 'playcount']
        if 'tags' in df.columns:
            columnas.append('tags')

        df = df[columnas]

        output_path = f"/opt/airflow/data/processed/lastfm_transformed{'_sample' if modo_prueba else ''}.parquet"
        df.to_parquet(output_path, index=False)

        print(f"{'🧪 (modo prueba)' if modo_prueba else '✅'} Last.fm transformado guardado en {output_path}")
        print(df)
        return df

    except Exception as e:
        print(f"❌ Error al transformar Last.fm: {e}")
        return None

if __name__ == "__main__":
    modo_prueba = "--test" in sys.argv
    transform_lastfm(modo_prueba)

