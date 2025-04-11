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

def transform_grammy(modo_prueba=True):
    input_path = "/opt/airflow/data/processed/grammy.parquet"

    try:
        df = pd.read_parquet(input_path)

        if modo_prueba:
            df = df.head(10)
            output_path = "/opt/airflow/data/processed/grammy_transformed_sample.parquet"
        else:
            output_path = "/opt/airflow/data/processed/grammy_transformed.parquet"

        df = df[['artist', 'year', 'category', 'nominee']]
        df['artist_normalized'] = df['artist'].apply(normalize_artist)
        df = df[df['artist_normalized'] != ""]
        df = df.drop_duplicates()

        # Agrupar por artista
        df_grouped = df.groupby('artist_normalized').agg({
            'artist': 'first',
            'year': lambda x: list(sorted(set(x))),
            'category': lambda x: list(sorted(set(x))),
            'nominee': lambda x: list(sorted(set(x))),
        }).reset_index()

        df_grouped['grammy_nominations'] = df_grouped['nominee'].apply(len)

        df_grouped.to_parquet(output_path, index=False)
        print(f"{'🧪 (modo prueba)' if modo_prueba else '✅'} Grammy transformado guardado en {output_path}")
        print(df_grouped)
        return df_grouped

    except Exception as e:
        print(f"❌ Error al transformar Grammy: {e}")
        return None

if __name__ == "__main__":
    modo_prueba = "--test" in sys.argv
    transform_grammy(modo_prueba)

