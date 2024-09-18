import os
import pandas as pd
from io import StringIO

# Ruta de la carpeta que contiene los CSVs
folder_path = '/Users/ochajin/Desktop/Prices/extract/comercio'

# Ruta para guardar el archivo consolidado
output_folder = '/Users/ochajin/Desktop/Prices/consolidated/comercio_output'
output_file = 'comercio_consolidado.csv'
output_path = os.path.join(output_folder, output_file)

# Asegurarse de que la carpeta de salida existe, si no, crearla
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Lista para almacenar los DataFrames
dataframes = []

# Función para limpiar un archivo CSV y eliminar la última fila
def clean_csv(file_path):
    # Leer el archivo CSV
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Eliminar la última fila
    lines = lines[:-1]

    # Lista para almacenar las líneas limpiadas
    cleaned_lines = []

    # Procesar línea por línea
    for i, line in enumerate(lines):
        if line.startswith("|"):
            cleaned_lines[-1] = cleaned_lines[-1].strip() + line
        else:
            cleaned_lines.append(line)

    # Guardar las líneas limpias en un nuevo DataFrame usando StringIO de io
    df = pd.read_csv(StringIO("".join(cleaned_lines)), delimiter='|')

    # Convertir la columna 'comercio_cuit' a string y eliminar filas vacías o con solo espacios
    if 'comercio_cuit' in df.columns:
        df['comercio_cuit'] = df['comercio_cuit'].astype(str)
        df = df[df['comercio_cuit'].str.strip() != '']  # Eliminar filas con comercio_cuit vacío

    # Convertir la columna 'id_comercio' a string y eliminar el '.0' al final si aparece
    if 'id_comercio' in df.columns:
        df['id_comercio'] = df['id_comercio'].astype(str).str.replace(r'\.0$', '', regex=True)

    # Convertir la columna 'id_bandera' a string y eliminar el '.0' al final si aparece
    if 'id_bandera' in df.columns:
        df['id_bandera'] = df['id_bandera'].astype(str).str.replace(r'\.0$', '', regex=True)

    # Eliminar filas con cualquier valor NaN
    df = df.dropna()

    return df

# Iterar sobre todos los archivos en la carpeta
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        df = clean_csv(file_path)
        if not df.empty:  # Verificar si el DataFrame no está vacío
            dataframes.append(df)

# Solo concatenar si hay DataFrames válidos en la lista
if dataframes:
    final_df = pd.concat(dataframes, ignore_index=True)
    # Guardar el archivo CSV final
    final_df.to_csv(output_path, index=False)
    print(f'Archivo consolidado guardado en: {output_path}')
else:
    print("No se encontraron archivos válidos para consolidar.")

import pandas as pd
import sqlite3

# Leer el CSV procesado (después de limpieza)
df = pd.read_csv(output_folder+"/"+output_file)

# Conectar a la base de datos
conn = sqlite3.connect('../database.db')

# Escribir el DataFrame en una tabla SQLite
df.to_sql('db_comercio', conn, if_exists='replace', index=False)

# Cerrar la conexión
conn.close()

print("Datos de comercio actualizados en la base de datos.")