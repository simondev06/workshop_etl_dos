import pandas as pd

# Ruta del archivo CSV
file_path = '../data/output/final_merged.csv'

# Leer el archivo CSV
df_final = pd.read_csv(file_path)

# Verifica la cantidad de valores nulos por cada columna
null_counts = df_final.isnull().sum()
print("Valores nulos por columna:")
print(null_counts)

# Verificar el tipo de datos por columna
print("\nTipos de datos por columna:")
print(df_final.dtypes)

# Mostrar las primeras 20 filas para ver si hay alguna irregularidad
print("\nPrimeras 20 filas del DataFrame:")
print(df_final.head(20))

# Comprobar el total de registros
print(f"\nTotal de registros en el DataFrame: {len(df_final)}")

