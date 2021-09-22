import random
import os

matriz = []
total = 3*10

os.system ("cls") 
for i in range (0,total,1):
    consonante = random.choice([" ","K","S","T","N","H","M","Y"])
    vocal = random.choice(["A","I","U","E","O"])
    silaba = consonante + vocal
    if (silaba == "YI" or silaba == "YE"):
        silaba="##"
#    print (silaba) 
    matriz.append(silaba)

for i in range (0,total,3):
    print (i, "\t", i+1,"\t", i+2, "\t", matriz[i] + "-" + matriz[i+1] + "-" + matriz[i+2])
                                        
