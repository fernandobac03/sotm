
from nltk.corpus import stopwords
from textblob import TextBlob
import pandas as pd
import numpy as np
from translate import traducir
import csv

#basico
datos = pd.read_csv('datos.csv')

#a minusculas 
datos['sugerencia_movilidad'] = datos['sugerencia_movilidad'].apply(lambda x: " ".join(x.lower() for x in x.split()))
datos['sugerencia_movilidad'].head()

#eliminando puntuacion
datos['sugerencia_movilidad'] = datos['sugerencia_movilidad'].str.replace('[^\w\s]','')
datos['sugerencia_movilidad'].head()

#traduciendo a ingles
datos['sugerencia_movilidad'] = datos['sugerencia_movilidad'].apply(lambda x: traducir(x)) 
datos['sugerencia_movilidad'].head()

#mi_path = "sugerencias-en.csv"
#f = open(mi_path, 'a+')

#for i in train['sugerencias_movilidad']:
#    f.write(i)
#    f.close()


with open("datos_en.csv", 'wb') as csv_file:
    csv_file.write("id_movilidad,correo,sugerencia_movilidad_en\n")
    for i in range(len(datos['id_movilidad'])):
        lineresult = str(datos['id_movilidad'][i]) + "," + str(datos['correo'][i]) + "," + str(datos['sugerencia_movilidad'][i])
        csv_file.write(lineresult + "\n")
        print lineresult
