import os
import hashlib
from collections import defaultdict

def find_duplicate_files(directory):
    """
    Busca archivos duplicados en un directorio y sus subdirectorios.

    Args:
        directory (str): El directorio a escanear.

    Returns:
        dict: Un diccionario donde las claves son los hashes de los archivos y los valores
              son listas de las rutas de los archivos con ese hash.
    """
    if not os.path.isdir(directory):
        print(f"Error: El directorio '{directory}' no existe.")
        return {}

    file_hashes = defaultdict(list)
    print("Buscando archivos duplicados. Esto puede tardar un poco...")
    
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # Calculamos el hash SHA-256 del archivo
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                file_hashes[file_hash].append(file_path)
            except (IOError, PermissionError) as e:
                # Ignoramos archivos que no podemos leer
                print(f"Advertencia: No se pudo leer el archivo '{file_path}': {e}")
                continue

    return {hash_val: paths for hash_val, paths in file_hashes.items() if len(paths) > 1}

def main():
    """
    Función principal para ejecutar el script.
    """
    # Se escanea el disco duro C:
    drive_to_scan = 'C:\\'
    
    print(f"Escaneando el disco duro '{drive_to_scan}' en busca de archivos duplicados...")
    
    # Busca los archivos duplicados
    duplicates = find_duplicate_files(drive_to_scan)
    
    if not duplicates:
        print("No se encontraron archivos duplicados.")
    else:
        print("\nArchivos duplicados encontrados:")
        print("-----------------------------------")
        for hash_val, paths in duplicates.items():
            print(f"Archivos con el mismo contenido (hash: {hash_val}):")
            for path in paths:
                print(f"  - {path}")
            print()

if __name__ == "__main__":
    main()
