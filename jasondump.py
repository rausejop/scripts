import csv, json

# Seguro que hay una forma mejor de hacerlo pero sirve como workaround rápido
# Guardar el xlsx de Excel en csv utf-8 delimitado por comas
# en Notepad++ sustituir todos los ; por , y grabar en codificación UTF-( sin BOM

csvFilePath= 'RECIN001.csv'
jsonFilePath= 'RECIN001.json'
data = {}

#fieldnames = ('id', 'DEV_ID','DEV_TIPO','DEV_DESCRIPCION','DEV_MARCA','DEV_MODELO','DEV_VERSION','DEV_FIRMWARE','DEV_OS','LOC_INSTALACION','DEV_OWNER_TEC','DEV_OWNER_BUSINESS','DEV_STATUS','DEV_OPERATION','DEV_MAINTENANCE','DEV_NOTAS','IP_MGMNT','CONF','INT','DISP','CRIT')
#print(fieldnames)

#import pandas as pd
#df = pd.read_csv(csvFilePath)
#print(df)

with open(csvFilePath, 'r', encoding='utf-8') as csvFile:
    csvReader = csv.DictReader(csvFile)
    for rows in csvReader:
        print("ROWS:\t", rows)
        clave = rows.get('id')
        print("CLAVE OK", clave)
        key = rows['id']
        data[key] = rows
        print('[', key, ']\t', rows)

with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:
    jsonFile.write(json.dumps(data, indent=4))

