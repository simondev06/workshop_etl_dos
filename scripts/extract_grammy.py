import pandas as pd
import sys

def extract_grammy_data(num_registros=1210):
    input_path = "/opt/airflow/data/raw/grammys/grammy.csv"
    output_path = "/opt/airflow/data/processed/grammy.parquet"

    try:
        df = pd.read_csv(input_path)

        # Filtrar por registros desde 2010
        df = df[df['year'] >= 2010]

        # Limitar el número de registros
        df = df.head(num_registros)

        df.to_parquet(output_path, index=False)
        print(f"✅ Grammy guardado en {output_path}")
        return df
    except FileNotFoundError:
        print("❌ Archivo no encontrado:", input_path)
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

if __name__ == "__main__":
    # Obtenemos num_registros desde los argumentos de la línea de comandos
    num_registros = int(sys.argv[1]) if len(sys.argv) > 1 else 1210  # Valor por defecto 1210
    extract_grammy_data(num_registros)

