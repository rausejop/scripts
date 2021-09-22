import os

contador = 0
f = open ("log_LongPaths.txt", "w")
linea = "[000]" + "\t" + "Ficheros con ruta mayor o igual a 240 caracteres: (1 unidad)+(2 :\\) + 256 + (1 null) = 260 caracteres\n"
print(linea)
f.write(linea)

for top, dirs, files in os.walk('C:\\'):
    for nm in files:
        ruta= os.path.join(top, nm)
        lenruta= len(ruta)
        linea = "["+ str(lenruta) + "]" + "\t" + ruta + "\n"
        if lenruta >=240:
            contador = contador +1
            print(linea)
            f.write(linea)
            linea = "[ddd]" + "\t" + "Ficheros con ruta mayor de 250 caracteres - 1 + 2 + 256 + 1 = 260\n"

linea = "[" + str(contador) +"]" + "\t" + "Ficheros con ruta mayor de 250 caracteres: (1 unidad)+(2 :\\) + 256 + (1 null) = 260 caracteres\n"
print(linea)
f.write(linea)
f.close()