import pandas as pd
import requests
import time
import unicodedata
import re
import sys
import ast

API_KEY = "3a3b93aa9fd93ed5351e863e1a51ebcf"
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def normalize_artist(name):
    if pd.isna(name):
        return ""
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    name = name.lower().strip()
    name = re.sub(r"[^\w\s]", "", name)
    return name

def get_artist_info(artist_name):
    params = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "artist" not in data:
            print(f"❌ No se encontró info para {artist_name}")
            return None

        artist = data["artist"]
        return {
            "artist": artist["name"],
            "artist_normalized": normalize_artist(artist["name"]),
            "listeners": artist.get("stats", {}).get("listeners"),
            "playcount": artist.get("stats", {}).get("playcount"),
            "tags": ", ".join([tag["name"] for tag in artist.get("tags", {}).get("tag", [])])
        }

    except Exception as e:
        print(f"  Error con {artist_name}: {e}")
        return None

def extract_lastfm_data(num_registros=1210):
    try:
        # Leer artistas desde Spotify
        df_spotify = pd.read_parquet("/opt/airflow/data/processed/spotify.parquet")

        spotify_artists = set()
        for raw in df_spotify['artists'].dropna():
            # Convertir string a lista si es necesario
            lista = ast.literal_eval(raw) if isinstance(raw, str) and raw.startswith("[") else [raw]
            if lista:
                primer_artista = normalize_artist(lista[0])
                spotify_artists.add(primer_artista)

        # Leer artistas desde Grammy
        df_grammy = pd.read_parquet("/opt/airflow/data/processed/grammy.parquet")
        grammy_artists = {normalize_artist(name) for name in df_grammy['artist'].dropna()}

        # Unir artistas de Spotify y Grammy
        all_artists = list(spotify_artists.union(grammy_artists))

        if len(all_artists) > num_registros:
            all_artists = all_artists[:num_registros]

        results = []
        for artist in all_artists:
            print(f"🔍 Consultando: {artist}")
            info = get_artist_info(artist)
            if info:
                results.append(info)
            time.sleep(0.2)

        df_result = pd.DataFrame(results)
        output_path = "/opt/airflow/data/processed/lastfm.parquet"
        df_result.to_parquet(output_path, index=False)
        print(f"✅ LastFM guardado en {output_path}")
        print(df_result)
        return df_result

    except Exception as e:
        print(f"❌ Error al extraer Last.fm: {e}")
        return None

if __name__ == "__main__":
    # Modo prueba por argumentos
    try:
        n = int(sys.argv[1])
    except:
        n = 1210
    extract_lastfm_data(num_registros=n)

