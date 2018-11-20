
from nltk.corpus import stopwords
from textblob import TextBlob
import pandas as pd
import numpy as np
from translate import traducir
import csv

#basico
train = pd.read_csv('/data/data/datos.csv')

#a minusculas 
train['sugerencia_movilidad'] = train['sugerencia_movilidad'].apply(lambda x: " ".join(x.lower() for x in x.split()))
train['sugerencia_movilidad'].head()

#eliminando puntuacion
train['sugerencia_movilidad'] = train['sugerencia_movilidad'].str.replace('[^\w\s]','')
train['sugerencia_movilidad'].head()

#traduciendo a ingles
train['sugerencia_movilidad'] = train['sugerencia_movilidad'].apply(lambda x: traducir(x)) 
#train['sugerencia_movilidad'].head()

#mi_path = "sugerencias-en.csv"
#f = open(mi_path, 'a+')

#for i in train['sugerencias_movilidad']:
#    f.write(i)
#    f.close()


with open("datos_en.csv", 'wb') as csv_file:
    csv_file.write("id_movilidad,correo,sugerencia_movilidad\n")
    for i in range(len(train['id_movilidad'])):
        lineresult = str(train['id_movilidad'][i]) + "," + str(train['correo'][i]) + "," + str(train['sugerencia_movilidad'][i])
        csv_file.write(lineresult + "\n")
        print lineresult
