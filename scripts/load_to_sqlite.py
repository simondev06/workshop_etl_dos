import pandas as pd
import os
import sqlite3
import sys

def load_to_sqlite(modo_prueba=True):
    try:
        suffix = "_sample" if modo_prueba else ""
        input_path = f"/opt/airflow/data/output/final_dataset{suffix}.parquet"
        db_path = "/opt/airflow/shared_data/merged_data.db"  # Ruta compartida con Windows
        table_name = "datos_finales"

        # Asegurar directorio
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Leer el archivo
        df = pd.read_parquet(input_path)
        print(f"✅ Archivo parquet leído: {input_path}")

        # Conectar y cargar en SQLite
        conn = sqlite3.connect(db_path)
        print(f"🔗 Conectado a la base de datos SQLite en {db_path}")
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"📦 Datos cargados en la tabla '{table_name}'")

        conn.close()
        print("✅ Conexión cerrada. Proceso de carga completado.")

    except Exception as e:
        print(f"❌ Error al cargar los datos: {e}")

if __name__ == "__main__":
    modo_prueba = "--test" in sys.argv
    load_to_sqlite(modo_prueba)

