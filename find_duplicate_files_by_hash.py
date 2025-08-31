#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Fichero: find_duplicate_files_by_hash.py
#
# Descripción: Script para escanear directorios y detectar archivos duplicados
#              basándose en el hash criptográfico (SHA-256) de su contenido.
#              Los mensajes por pantalla usan loguru y la salida a fichero
#              usa formato ISO 8601.
# Autor:       Rafael Ausejo Prieto
# Fecha:       31 de agosto de 2025
# Versión:     2.0.0
#
# Historial de Versiones:
#   1.0.0 - 11/08/2025: Implementación inicial del escaneo de duplicados.
#   2.0.0 - 31/08/2025: Añadida lista de directorios exentos de verificación.
#                       Refactorización para usar argparse.
#                       Añadida barra de progreso utilizando la librería tqdm.
#                       Optimizado el algoritmo para evitar el escaneo de
#                           directorios excluidos, usando la poda de os.walk.
#                       Añadido Loguru para mensajes por pantalla
#                       Añadido fichero de salida con formato ISO 8601.
#                       Código adecuado a normas de estilo PEP 8 y PEP 257.
#                       Optimización SWBOK con escaneo en una sola pasada
#                       Optimización SWBOK para hash incremental de archivos
#                           grandes usando 64ks de búfer sin consumir RAM
#                       Optimización SWBOK para  poda de directorio, evitando
#                           descender en subdirectorios en exclusión.
#
# Licencia: Apache License 2.0

import hashlib
import argparse
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from loguru import logger
from tqdm import tqdm

# Desactivar el manejador por defecto de loguru para usar uno personalizado
logger.remove()
# Configurar la salida de loguru con colores para la consola
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# Constantes para la versión y el manpage
VERSION = "3.0.0"
# Tamaño del bloque para el cálculo del hash
BUFFER_SIZE = 65536  # 64KB

# La cabecera del manpage
MANPAGE = f"""
NOMBRE
    find_duplicate_files_by_hash.py - Escanea directorios en busca de archivos duplicados.

SINOPSIS
    python find_duplicate_files_by_hash.py [OPCIONES]

DESCRIPCIÓN
    find_duplicate_files_by_hash.py es una herramienta de línea de comandos para
    encontrar archivos duplicados en un directorio y sus subdirectorios. La
    detección se realiza calculando el hash criptográfico (SHA-256) de cada archivo
    y agrupando aquellos con el mismo hash.

    El script está optimizado para evitar el escaneo de directorios del sistema
    o cualquier otra ruta especificada en un archivo de exclusión. Utiliza un
    algoritmo de una sola pasada para mayor eficiencia y procesa los archivos
    en bloques para un uso óptimo de la memoria.

OPCIONES
    -h, --help
        Muestra este manpage y sale.

    -v, --version
        Muestra la versión del script y sale.

    -d, --directory <directorio>
        Especifica el directorio raíz a escanear. Si no se proporciona, el
        script escaneará el directorio actual (.).

    -e, --exclude-file <fichero>
        Proporciona la ruta a un archivo de texto que contiene una lista de
        directorios a excluir del escaneo. Cada directorio debe estar en una
        línea separada. Si este parámetro no se usa, el script utilizará una
        lista de directorios del sistema por defecto.

    -o, --output-file <fichero>
        Especifica el nombre del archivo de salida donde se guardarán los
        resultados. Si no se proporciona, el valor por defecto es 'duplicados.txt'.

EJEMPLOS
    1. Escanea el directorio actual y guarda los resultados por defecto:
        python find_duplicate_files_by_hash.py

    2. Escanea el directorio "C:\\" y guarda los resultados en un archivo específico:
        python find_duplicate_files_by_hash.py -d "C:\\" -o "C:\\resultados.txt"

    3. Escanea un directorio específico, usando una lista de exclusión personalizada:
        Crea un archivo 'exclude.txt' con, por ejemplo, 'C:\\ProgramData' en una
        línea y 'C:\\Users\\tu_usuario\\AppData' en otra. Luego ejecuta:
        python find_duplicate_files_by_hash.py -d "C:\\" -e "exclude.txt"

AUTHOR
    Rafael Ausejo Prieto
    Fecha de Creación: 31 de agosto de 2025
    Versión: {VERSION}
"""

# Constantes para las exclusiones por defecto
DEFAULT_EXCLUDE_DIRS = [
    Path("C:\\Windows"),
    Path("C:\\Program Files"),
    Path("C:\\Program Files (x86)"),
    Path("C:\\$Recycle.Bin"),
    Path("C:\\hiberfil.sys"),
    Path("C:\\pagefile.sys"),
    Path("C:\\swapfile.sys"),
    Path("C:\\DumpStack.log.tmp"),
]


def load_exclude_list(file_path: Path) -> list[Path]:
    """
    Lee las rutas de directorios a excluir desde un archivo de texto.

    Args:
        file_path (Path): Ruta al archivo de texto.

    Returns:
        list[Path]: Una lista de rutas de directorios.
    """
    if file_path and not file_path.is_file():
        logger.warning(f"Advertencia: El archivo de exclusión '{file_path}' no se encontró. Usando la lista por defecto.")
        return DEFAULT_EXCLUDE_DIRS

    if not file_path:
        logger.info("No se ha proporcionado un archivo de exclusión. Usando la lista por defecto.")
        return DEFAULT_EXCLUDE_DIRS

    logger.info(f"Cargando la lista de exclusión desde '{file_path}'...")
    try:
        with file_path.open('r', encoding='utf-8') as f:
            # Normaliza las rutas y las convierte a objetos Path
            return [Path(line.strip()).resolve() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Error al leer el archivo de exclusión: {e}. Usando la lista por defecto.")
        return DEFAULT_EXCLUDE_DIRS


def calculate_hash(file_path: Path) -> str | None:
    """
    Calcula el hash SHA-256 de un archivo en bloques.

    Args:
        file_path (Path): La ruta al archivo.

    Returns:
        str | None: El hash SHA-256 del archivo como string hexadecimal, o None si hay un error.
    """
    try:
        hasher = hashlib.sha256()
        with file_path.open('rb') as f:
            while chunk := f.read(BUFFER_SIZE):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, PermissionError) as e:
        logger.warning(f"No se pudo leer el archivo '{file_path}': {e}")
        return None


def find_duplicate_files(directory: Path, exclude_dirs: list[Path] = None) -> dict:
    """
    Busca archivos duplicados en un directorio y sus subdirectorios en una
    sola pasada, usando poda de directorios excluidos.

    Args:
        directory (Path): Directorio a escanear.
        exclude_dirs (list[Path]): Lista de rutas de directorios a excluir.

    Returns:
        dict: Diccionario donde las claves son los hashes de los archivos y los
              valores son las rutas de los archivos con ese hash.
    """
    if not directory.is_dir():
        logger.error(f"El directorio '{directory}' no existe o no es accesible.")
        return {}

    file_hashes = defaultdict(list)
    exclude_dirs = [d.resolve() for d in exclude_dirs or []]

    # Recorrido único con tqdm y poda de directorios
    logger.info("Escaneando y calculando hashes. Esto puede tardar un poco...")
    with tqdm(desc="Escaneando archivos", unit=" archivos") as pbar:
        # Usamos Path.walk() que es más "Pythonic" y optimizado para este caso
        for dirpath, dirnames, filenames in Path(directory).walk():
            # Poda de directorios: Modifica 'dirnames' in-place para que walk() no entre
            dirnames[:] = [d for d in dirnames if not any((dirpath / d).resolve().is_relative_to(excluded) for excluded in exclude_dirs)]
            
            for filename in filenames:
                file_path = dirpath / filename
                # Asegurarse de que el archivo no está en un subdirectorio excluido
                if not any(file_path.resolve().is_relative_to(excluded) for excluded in exclude_dirs):
                    file_hash = calculate_hash(file_path)
                    if file_hash:
                        file_hashes[file_hash].append(file_path)
                    pbar.update(1)
                else:
                    logger.debug(f"Saltando archivo en directorio excluido: '{file_path}'")

    return {hash_val: paths for hash_val, paths in file_hashes.items() if len(paths) > 1}


def main():
    """Función principal para ejecutar el script de búsqueda de duplicados."""
    # Configurar el analizador de argumentos
    parser = argparse.ArgumentParser(
        description=MANPAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # Se añade la ayuda y la versión como acciones estándar
    parser.add_argument("-v", "--version", action="version", version=f"find_duplicate_files_by_hash.py v{VERSION}")
    parser.add_argument("-d", "--directory", type=Path, default=Path("."),
                        help="Especifica el directorio raíz a escanear. Por defecto: '.'")
    parser.add_argument("-e", "--exclude-file", type=Path,
                        help="Ruta a un archivo con directorios a excluir.")
    parser.add_argument("-o", "--output-file", type=Path, default=Path("duplicados.txt"),
                        help="Nombre del archivo de salida. Por defecto: 'duplicados.txt'")

    args = parser.parse_args()

    exclude_list = load_exclude_list(args.exclude_file)
    logger.info(f"Escaneando el directorio '{args.directory.resolve()}' en busca de archivos duplicados...")
    
    # Asegúrate de que los directorios excluidos se resuelvan antes de pasarlos a la función
    resolved_exclude_list = [d.resolve() for d in exclude_list]
    logger.info(f"Se excluirán {len(resolved_exclude_list)} directorios.")

    duplicates = find_duplicate_files(args.directory, exclude_dirs=resolved_exclude_list)

    if not duplicates:
        logger.success("No se encontraron archivos duplicados. ✅")
    else:
        logger.info(f"Se encontraron archivos duplicados. Guardando resultados en '{args.output_file}'... 📝")
        try:
            with args.output_file.open('w', encoding='utf-8') as f:
                for hash_val, paths in duplicates.items():
                    f.write(f"--- Duplicados con hash: {hash_val} ---\n")
                    for path in paths:
                        timestamp = datetime.now().isoformat()
                        f.write(f"{timestamp} | Archivo duplicado: {path}\n")
                    f.write("\n")
            logger.success("Resultados guardados con éxito. ✅")
        except IOError as e:
            logger.error(f"Error: No se pudo escribir en el archivo '{args.output_file}': {e} ❌")


if __name__ == "__main__":
    main()