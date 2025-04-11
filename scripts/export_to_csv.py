import pandas as pd
import os
import sys

def export_to_csv(modo_prueba=True):
    try:
        suffix = "_sample" if modo_prueba else ""
        input_path = f"/opt/airflow/data/processed/final_merged{suffix}.parquet"
        output_dir = "/opt/airflow/data/output"
        output_path = os.path.join(output_dir, f"final_merged{suffix}.csv")

        os.makedirs(output_dir, exist_ok=True)

        df = pd.read_parquet(input_path)
        print(f"✅ Leído: {input_path}")

        df.to_csv(output_path, index=False)
        print(f"📤 Exportado como CSV en: {output_path}")

    except Exception as e:
        print(f"❌ Error al exportar a CSV: {e}")

if __name__ == "__main__":
    modo_prueba = "--test" in sys.argv
    export_to_csv(modo_prueba)

