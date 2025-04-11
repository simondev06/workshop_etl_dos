import pandas as pd

def contar_registros_spotify():
    try:
        # Ruta del archivo
        input_path = "../data/processed/spotify.parquet"
        
        # Leer el archivo Parquet
        df = pd.read_parquet(input_path)
        
        # Contar el número de registros
        num_registros = len(df)
        
        print(f"El archivo de Spotify tiene {num_registros} registros.")
        return num_registros
    
    except Exception as e:
        print(f"❌ Error al contar registros: {e}")
        return None

if __name__ == "__main__":
    contar_registros_spotify()

