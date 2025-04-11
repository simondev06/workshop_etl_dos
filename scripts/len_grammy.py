import pandas as pd

# Ruta del archivo CSV de Grammy
input_path_grammy = "../data/raw/grammys/grammy.csv"

# Cargar el CSV en un DataFrame
df_grammy = pd.read_csv(input_path_grammy)

# Filtrar por los años de los Grammy (de 2010 hacia adelante)
df_grammy_filtered = df_grammy[df_grammy['year'] >= 2010]

# Ver cuántos registros quedan después del filtro
print(f"Cantidad de registros en el dataset Grammy (2010 en adelante): {len(df_grammy_filtered)}")

