import argparse # Importamos el módulo argparse para procesar argumentos de linea de comandos
from loguru import logger # Importamos el módulo loguru para registrar logs detallados
import cv2 # Importamos OpenCV para leer y procesar el archivo de video .mp4
import os # Importamos el módulo os para trabajar con archivos en disco
import numpy as np # Importamos numpy para el cálculo numérico y la sustracción de imágenes
from PIL import Image # Importamos el módulo Image de Pillow para crear un único PDF final
import sys # Importamos sys para configuración de sistema o salida

# Inicializamos el logger para que registre la hora, el nivel y el mensaje
logger.info("Configurando motor de dependencias (argparse, loguru, cv2, os, numpy, PIL).")

# Definimos la función principal que ejecutará toda la lógica
def main():
    # Creamos un parser para leer argumentos de línea de comandos
    logger.info("Instanciando ArgumentParser para procesar opciones.")
    parser = argparse.ArgumentParser(description="Extrae frames únicos de un video MP4 y los convierte a PDF.")
    
    # Agregamos el argumento que exigirá la ruta del archivo MP4
    logger.info("Añadiendo el argumento 'video' obligatorio al parser.")
    parser.add_argument("video", help="El nombre o ruta del fichero .mp4 a procesar")
    
    # Parseamos los argumentos provistos por el usuario en consola
    logger.info("Leyendo y parseando los argumentos del usuario.")
    args = parser.parse_args()
    
    # Capturamos la ruta del video en una variable
    logger.info(f"Ruta o nombre del video proveída por parámetro: {args.video}")
    video_path = args.video
    
    # Comprobamos si el fichero suministrado existe realmente en el disco
    logger.info(f"Comprobando si existe el fichero: {video_path}")
    if not os.path.exists(video_path):
        # Registramos un error si no lo encontramos
        logger.error("El fichero de video especificado no existe. Abortando ejecución.")
        # Salimos del programa devolviendo un código de error
        sys.exit(1)
        
    # Inicializamos la utilidad VideoCapture de OpenCV pasándole el archivo
    logger.info("Iniciando la lectura del archivo de video usando cv2.VideoCapture().")
    cap = cv2.VideoCapture(video_path)
    
    # Obtenemos los fotogramas por segundo que tiene el video (FPS)
    logger.info("Obteniendo valor de fotogramas por segundo (FPS).")
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Si por algún motivo no obtenemos el valor o es menor a 1, forzamos un valor por defecto de 30
    logger.info("Verificando si la variable FPS es nula o menor a 1 para setear valor por defecto.")
    if not fps or fps < 1:
        # Asignamos 30 fps
        logger.info("FPS inválido detectado, seteando FPS por defecto a 30.")
        fps = 30.0
        
    # Extraemos el total de fotogramas que componen el vídeo completo
    logger.info("Contando el total de fotogramas existentes en todo el archivo de vídeo.")
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Creamos un log para que el usuario conozca los metadatos del vídeo
    logger.info(f"Metadatos extraídos - FPS: {fps:.2f}, Frames Totales: {frame_count}")
    
    # Leemos obligatoriamente el primer fotograma del vídeo para usarlo de referencia inicial
    logger.info("Intentando extraer el primer fotograma absoluto (frame 0) del video.")
    success, frame = cap.read()
    
    # Comprobamos si la lectura del primer fotograma falló
    logger.info("Comprobando si la lectura del primer fotograma fue exitosa ('success').")
    if not success:
        # Generamos un error en loguru si falla la lectura del video
        logger.error("No se pudo leer ningún fotograma del archivo MP4 suministrado.")
        # Finalizamos la ejecución forzosamente
        sys.exit(1)
        
    # Configuramos nuestro contador para las imágenes JPG que irán generándose (empezamos por 1)
    logger.info("Iniciando variable 'image_idx' en 1 para nombrar el primer JPG.")
    image_idx = 1
    
    # Nombramos la ruta que va a tener nuestra primera imagen generada
    logger.info("Generando string con el nombre del archivo JPG (001.jpg).")
    img_name = f"{image_idx:03d}.jpg"
    
    # Escribimos el primer fotograma en disco obligatoriamente (es la primera diapositiva)
    logger.info(f"Guardando la primera diapositiva en el disco como {img_name}.")
    cv2.imwrite(img_name, frame)
    
    # Creamos una lista para ir almacenando los nombres de todos los archivos JPG guardados
    logger.info("Creando lista 'jpg_list' vacía para registrar las imágenes guardadas.")
    jpg_list = []
    
    # Añadimos el primer frame a nuestra lista de recolección de JPG
    logger.info("Añadiendo el primer JPG a nuestra lista de seguimiento de archivos finales.")
    jpg_list.append(img_name)
    
    # Convertimos el fotograma de BGR a Escala de Grises para comparación mas rápida
    logger.info("Convirtiendo primer frame a Escala de Grises (COLOR_BGR2GRAY) para cálculo eficiente.")
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Redimensionamos la imagen en gris para que comparar el contenido no consuma mucha memoria (160x120)
    logger.info("Redimensionando frame gris a resolución muy baja (160x120) para mayor velocidad de resta.")
    prev_frame = cv2.resize(gray_frame, (160, 120))
    
    # Establecemos nuestro umbral numérico empírico que determina si la diapositiva ha cambiado significativamente
    logger.info("Definiendo umbral de diferencia de píxeles a valor 12.0 (slider threshold).")
    threshold = 12.0
    
    # Establecemos el salto de frames por iteración a la cantidad de FPS (evaluamos 1 vez cada 2 segundos aprox.)
    logger.info("Calculando el salto temporal 'step' multiplicando FPS x 2 (analisis de fotogramas espaciados).")
    step = int(fps * 2) 
    
    # Definimos nuestra variable de fotograma actual, donde reiniciamos en nuestro cursor = 0
    logger.info("Seteando cursor de iteración 'current_frame' a 0 para el bucle.")
    current_frame = 0
    
    # Iniciamos el bucle condicional para recorrer todo el video, saltando fotogramas según paso
    logger.info("Empezando el bucle de procesamiento 'while current_frame < frame_count'.")
    while current_frame < frame_count:
        # Le indicamos al motor de OpenCV que salte al fotograma indicado
        logger.info(f"Situando cabezal virtual de video en el fotograma exacto N.º {current_frame}.")
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        
        # Leemos los datos de ese fotograma explícito
        logger.info(f"Leyendo efectivamente fotograma de la posición {current_frame}.")
        success, frame = cap.read()
        
        # Comparamos fallos de buffer
        logger.info("Verificando variable de exito 'success' de este buffer.")
        if not success:
            # Adelantamos si el salto rebasó la linea o fue corrupto
            logger.info("Fallo en la lectura de buffer actual. Saltando internamente.")
            current_frame += step
            # Reiniciamos vuelta algorítmica
            logger.info("Disparando comando 'continue' al bucle del parser de frame.")
            continue
            
        # Convertimos fotograma iterativo a matriz simple en blanco y negro
        logger.info("Transformando iteración visual a cv2.COLOR_BGR2GRAY.")
        gray_iter = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Reducción matricial
        logger.info("Ejecutando resizing a (160, 120) a la nueva captura base en escala de grises.")
        scaled_iter = cv2.resize(gray_iter, (160, 120))
        
        # Cálculo de tensor delta con medias absolutas float de np
        logger.info("Sumando diferencia np.mean(np.abs(anterior - iteracion)) para buscar el delta computacional.")
        diff = np.mean(np.abs(scaled_iter.astype(np.float32) - prev_frame.astype(np.float32)))
        
        # Comparamos magnitud del del delta 
        logger.info(f"Validando si varianza obtenida ({diff:.2f}) es abismal (> umbral de {threshold:.2f}).")
        if diff > threshold:
            # Nuevo Slide detectado
            logger.info(f"¡Cambio fuerte en la escena detectado! Incrementando variable global 'image_idx' = {image_idx + 1}.")
            image_idx += 1
            
            # Interpolación String a 00N
            logger.info("Estableciendo template string de enumeración paddeada a 3 ceros de la nueva vista.")
            img_name = f"{image_idx:03d}.jpg"
            
            # Exportación cruda disco
            logger.info(f"Forzando persistencia CV2 a disco rígido por invocación cv2.imwrite() sobre: {img_name}.")
            cv2.imwrite(img_name, frame)
            
            # Anexión en variable matriz final
            logger.info(f"Apelando append() de {img_name} sobre nuestra estructura maestra de arrays.")
            jpg_list.append(img_name)
            
            # Refresco de referencia comparativa
            logger.info("Desplazando 'prev_frame' a este estado 'scaled_iter' para servir de faro a los proximos escaneos de tiempo.")
            prev_frame = scaled_iter
            
        # Refrescamos bucle temporal 1 iteración real vs la de OpenCV
        logger.info(f"Agregando a 'current_frame' ({current_frame}) el coeficiente métrico de salto ({step}).")
        current_frame += step

    # Ya escaneado, soltamos control de archivo
    logger.info("Cerrando proceso nativo mp4 y liberando handlers de archivo en OS del host con 'release()'.")
    cap.release()
    
    # Verificamos si logramos un resultado real
    logger.info(f"Recuento final de capturas obtenidas evaluando len() de lista nativa: total de {len(jpg_list)} items.")
    if not jpg_list:
        # Saliendo y registrando empty log
        logger.warning("No hubo imágenes significativas para formar el documento. Terminado vacío.")
        return
        
    # Agrupamos PIL
    logger.info("Definiendo estructura abstracta 'images_to_pdf' de Python nativo lista[].")
    images_to_pdf = []
    
    # Loop convertidor JPG
    logger.info("Empezando el for-loop para reconversión a PDF PIL.")
    for file_path in jpg_list:
        # Instancia unitaria
        logger.info(f"Ejecutando asignación virtual Image.open() local sobre: {file_path}.")
        img = Image.open(file_path)
        
        # Limpieza RGB
        logger.info(f"Re-mapeando modo de coloración de buffer a 'RGB' (canal Alpha nulo) del recurso fotográfico {file_path}.")
        img_rgb = img.convert('RGB')
        
        # Carga en vector de memoria
        logger.info("Enlistando instancia procesada 'img_rgb' adentro del stack de memoria de conversion hacia PDF.")
        images_to_pdf.append(img_rgb)
        
    # Bautizando PDF final con el mismo nombre y .pdf
    logger.info("Configurando el nombre de salida basado en el valor OS os.path.splitext() restándole extensión final '.mp4' y asignando '.pdf'.")
    output_pdf_name = os.path.splitext(os.path.basename(video_path))[0] + ".pdf"
    
    # Volcado multi paginado
    logger.info(f"Desencadenando protocolo 'save_all=True' desde images_to_pdf[0] y apuntando hacia el output de nombre '{output_pdf_name}'.")
    images_to_pdf[0].save(
        output_pdf_name,
        save_all=True,
        append_images=images_to_pdf[1:],
        resolution=100.0
    )
    
    # Emisión final exitosa en la pantalla
    logger.info(f"[PROCESO TERMINADO CON EXITO]: Creado el consolidado multi-documento con un total de {len(jpg_list)} páginas y nombre '{output_pdf_name}'.")

# Bloque default arranque scripts Python Main
logger.info("Verificando protocolo de punto de entrada (__name__ == '__main__').")
if __name__ == "__main__":
    logger.info("Instruyendo ejecución final del core en main() explícito.")
    main()
