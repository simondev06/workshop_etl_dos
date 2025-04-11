import pandas as pd
import numpy as np
import unicodedata
import re

# -------------------------------
# Función para normalizar nombres de artista
# -------------------------------
def normalize_artist(artist):
    if isinstance(artist, str):
        artist = artist.lower()
        artist = unicodedata.normalize('NFKD', artist)
        artist = ''.join(c for c in artist if not unicodedata.combining(c))
        artist = re.sub(r'[^a-z0-9\s]', '', artist)
        artist = re.sub(r'\s+', ' ', artist).strip()
        return artist
    return None

# -------------------------------
# Cargar datasets
# -------------------------------
print("📥 Cargando datasets...")
df_spotify = pd.read_parquet("/opt/airflow/data/processed/spotify_transformed.parquet")
df_grammy  = pd.read_parquet("/opt/airflow/data/processed/grammy_transformed.parquet")
df_lastfm  = pd.read_parquet("/opt/airflow/data/processed/lastfm_transformed.parquet")
print("✅ Carga completada.")

# -------------------------------
# Normalizar y ajustar columna de artista en Spotify
# -------------------------------
# Si existe la columna "artists", la renombramos a "artist"
if "artists" in df_spotify.columns:
    df_spotify = df_spotify.rename(columns={"artists": "artist"})
elif "artist" not in df_spotify.columns:
    raise ValueError("❌ No se encontró ninguna columna que contenga el nombre del artista en Spotify.")

# Ahora, convertir la columna "artist" a string plano:
df_spotify["artist"] = df_spotify["artist"].apply(lambda x: x[0] if isinstance(x, (list, np.ndarray)) and len(x) > 0 else str(x))
df_spotify["artist_normalized"] = df_spotify["artist"].apply(normalize_artist)

# Normalizar en Grammy y Last.fm (ya tienen "artist" como string)
df_grammy["artist_normalized"] = df_grammy["artist"].apply(normalize_artist)
df_lastfm["artist_normalized"] = df_lastfm["artist"].apply(normalize_artist)

# -------------------------------
# Agrupar datasets
# -------------------------------
print("📊 Agrupando Spotify...")
df_spotify_grouped = df_spotify.groupby("artist_normalized").agg({
    "artist": "first",
    "album_name": lambda x: list(pd.unique(x.dropna())),
    "track_name": lambda x: list(pd.unique(x.dropna())),
    "track_genre": lambda x: list(pd.unique(x.dropna())),
    "popularity": "mean"
}).reset_index()

print("🏆 Agrupando Grammy...")
# Aquí, dado que en Grammy algunas columnas (year, category, nominee) son arrays, las procesamos:
df_grammy_grouped = df_grammy.groupby("artist_normalized").agg({
    "year": lambda x: list(pd.unique(sum([list(item) if isinstance(item, (list, np.ndarray)) else [item] for item in x.dropna()], []))),
    "category": lambda x: list(pd.unique(sum([list(item) if isinstance(item, (list, np.ndarray)) else [item] for item in x.dropna()], []))),
    "nominee": lambda x: list(pd.unique(sum([list(item) if isinstance(item, (list, np.ndarray)) else [item] for item in x.dropna()], []))),
}).reset_index()

# En este agrupamiento, calculamos las nominaciones como la cantidad de nominaciones únicas
df_grammy_grouped["grammy_nominations"] = df_grammy_grouped["nominee"].apply(lambda x: len(x) if isinstance(x, list) else 0)

print("📊 Agrupando Last.fm...")
df_lastfm_grouped = df_lastfm.groupby("artist_normalized").agg({
    "listeners": "mean",
    "playcount": "mean",
    "tags": "first"  # O bien podrías agregar otra función de agrupamiento si es necesario
}).reset_index()

# -------------------------------
# Realizar Merges
# -------------------------------
print("🔀 Uniendo Spotify y Grammy...")
df_merged = pd.merge(df_spotify_grouped, df_grammy_grouped, how="left", on="artist_normalized")

print("📈 Uniendo con Last.fm...")
df_merged = pd.merge(df_merged, df_lastfm_grouped, how="left", on="artist_normalized")

# -------------------------------
# Limpiar columnas innecesarias (si quedaron de merges anteriores)
# -------------------------------
cols_a_eliminar = ["artist_normalized_x", "artist_normalized_y", "track_id", "Unnamed: 0", "time_signature"]
df_merged.drop(columns=[col for col in cols_a_eliminar if col in df_merged.columns], inplace=True)
df_merged['grammy_nominations'] = df_merged['grammy_nominations'].fillna(0).astype(int)
# -------------------------------
# Guardar resultado final
# -------------------------------
print("💾 Guardando dataset final...")
df_merged.to_parquet("/opt/airflow/data/output/final_dataset.parquet", index=False)
print("✅ Dataset final guardado exitosamente.")

