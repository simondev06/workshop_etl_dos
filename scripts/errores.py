import pandas as pd
import numpy as np

def revisar_columna_artista(df, nombre_dataset, columna_artista):
    print(f"\n🔍 Revisando columna de artista en {nombre_dataset}...")

    if columna_artista not in df.columns:
        print(f"❌ La columna '{columna_artista}' no existe en {nombre_dataset}")
        return

    ejemplos = df[columna_artista].head(5).tolist()
    tipos = df[columna_artista].apply(type).value_counts()

    print(f"✅ Ejemplos de '{columna_artista}':")
    for ej in ejemplos:
        print("  ", ej)
    
    print(f"\n📊 Tipos de datos en '{columna_artista}':")
    print(tipos)


# Cargamos los datasets
path_grammy = "../data/processed/grammy_transformed.parquet"
path_lastfm = "../data/processed/lastfm_transformed.parquet"

df_grammy = pd.read_parquet(path_grammy)
df_lastfm = pd.read_parquet(path_lastfm)

# Revisamos las columnas relevantes
revisar_columna_artista(df_grammy, "Grammy", "artist")
revisar_columna_artista(df_grammy, "Grammy", "nominee")

revisar_columna_artista(df_lastfm, "LastFM", "artist")

