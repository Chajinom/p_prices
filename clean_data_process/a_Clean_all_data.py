import subprocess

# Lista de scripts a ejecutar
scripts = [ 'unZip_Data.py','Cleanup_comercio.py', 'Cleanup_Productos.py', 'Cleanup_Sucursal.py']

# Función para ejecutar los scripts
def run_all_scripts(scripts):
    for script in scripts:
        try:
            # Ejecutar el script usando subprocess y capturar la salida
            print(f"Ejecutando {script}...")
            result = subprocess.run(['python3', script], capture_output=True, text=True)
            # Mostrar la salida del script
            if result.stdout:
                print(f"Salida de {script}:\n{result.stdout}")
            if result.stderr:
                print(f"Errores de {script}:\n{result.stderr}")

        except Exception as e:
            print(f"Error al ejecutar {script}: {e}")

# Ejecutar los scripts
run_all_scripts(scripts)