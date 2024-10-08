import os
import pandas as pd
from io import StringIO

# Ruta de la carpeta que contiene los CSVs
folder_path = '/Users/ochajin/Desktop/Prices/extract/sucursales'

# Ruta para guardar el archivo consolidado
output_folder = '/Users/ochajin/Desktop/Prices/consolidated/sucursales_output'
output_file = 'sucursales_consolidado.csv'
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
    return df

# Iterar sobre todos los archivos en la carpeta
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        df = clean_csv(file_path)
        dataframes.append(df)

# Consolidar todos los DataFrames en uno solo
final_df = pd.concat(dataframes, ignore_index=True)

# Guardar el archivo CSV final
final_df.to_csv(output_path, index=False)

print(f'Archivo consolidado guardado en: {output_path}')

import pandas as pd
import sqlite3

# Leer el CSV procesado (después de limpieza)
df = pd.read_csv(output_folder+"/"+output_file)

# Conectar a la base de datos
conn = sqlite3.connect('../database.db')

# Escribir el DataFrame en una tabla SQLite
df.to_sql('db_sucursal', conn, if_exists='replace', index=False)

# Cerrar la conexión
conn.close()

print("Datos de sucursal actualizados en la base de datos.")