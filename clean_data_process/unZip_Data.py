import os
import zipfile
import shutil
from pathlib import Path

# Definir la ruta de la carpeta que contiene el archivo ZIP
ruta_carpeta = '/Users/ochajin/Desktop/Prices/download/'

# Buscar el archivo ZIP en la carpeta
archivo_zip_principal = None
for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith('.zip'):
        archivo_zip_principal = os.path.join(ruta_carpeta, archivo)
        break

# Asegúrate de que se encontró un archivo ZIP
if archivo_zip_principal is None:
    raise FileNotFoundError("No se encontró un archivo ZIP en la carpeta especificada.")

# Definir la ruta de extracción
#ruta_extraccion = os.path.join(ruta_carpeta, 'extraccion')
ruta_extraccion = '/Users/ochajin/Desktop/Prices/extract/'

# Asegúrate de que la carpeta de extracción exista
os.makedirs(ruta_extraccion, exist_ok=True)


def extraer_zip_anidado(archivo_zip, ruta_destino, prefijo=""):
    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        for archivo in zip_ref.namelist():
            # Si el archivo es otro ZIP, extraerlo recursivamente
            if archivo.endswith('.zip'):
                nuevo_prefijo = prefijo + Path(archivo).stem + "_"
                ruta_zip_interno = os.path.join(ruta_destino, archivo)
                zip_ref.extract(archivo, ruta_destino)
                extraer_zip_anidado(ruta_zip_interno, ruta_destino, nuevo_prefijo)
                os.remove(ruta_zip_interno)  # Elimina el ZIP interno después de extraer
            # Si es un CSV, extraerlo, renombrarlo y moverlo a la carpeta correspondiente
            elif archivo.endswith('.csv'):
                nombre_archivo = Path(archivo).stem
                nombre_nuevo = prefijo + nombre_archivo + ".csv"

                # Determinar la carpeta de destino según el nombre del archivo
                carpeta_destino = os.path.join(ruta_destino, nombre_archivo)
                os.makedirs(carpeta_destino, exist_ok=True)

                ruta_csv = os.path.join(carpeta_destino, nombre_nuevo)
                zip_ref.extract(archivo, ruta_destino)
                shutil.move(os.path.join(ruta_destino, archivo), ruta_csv)


# Ejecutar la función
extraer_zip_anidado(archivo_zip_principal, ruta_extraccion)