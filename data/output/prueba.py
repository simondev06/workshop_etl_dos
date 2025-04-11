import pandas as pd

# Ruta del archivo CSV
file_path = './final_dataset.parquet'

# Leer el archivo CSV
df_final = pd.read_parquet(file_path)

# Mostrar las primeras 20 filas
print(df_final.head(50))
