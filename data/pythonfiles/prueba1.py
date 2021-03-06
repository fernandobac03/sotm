# coding=utf-8
from nltk.corpus import stopwords
from textblob import TextBlob
import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import requests
from translate import traducir
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
import unicodedata 



def elimina_tildes(texto):
    string_acentos = texto.decode('utf-8')

    s = "".join((c for c in unicodedata.normalize('NFD',unicode(string_acentos)) if unicodedata.category(c) != 'Mn'))
    return s.decode()

#basico
datos = pd.read_csv('datos_es_en.csv')
datos['word_count'] = datos['sugerencia_en'].apply(lambda x: len(str(x).split(" ")))
datos[['sugerencia_en', 'word_count']].head()

#eliminando stopwords
#new_stopwords = set(stopwords.words('es')) - {'me', 'se', 'mas', 'deberia', 'deberian'}
stop = stopwords.words('spanish')
datos['cleaned'] = datos['sugerencia_en'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
datos[['sugerencia_en', 'cleaned']].head()

#eliminando palabras raras
freq = pd.Series(' '.join(datos['cleaned']).split()).value_counts()[-10:]
freq = list(freq.index)
datos['cleaned'] = datos['cleaned'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
datos[['sugerencia_en', 'cleaned']].head()


#ortografia
#train['cleaned'] = train['cleaned'].apply(lambda x: str(TextBlob(x).correct()))
#train[['sugerencia_movilidad', 'cleaned']].head()

#stemming , eliminando  terminaciones de palabras ing, ly, etc. no se si trabaja para espaniol
#st = PorterStemmer()
#train['stemming'] = train['cleaned'].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))
#train[['cleaned','stemming']].head()


#limpiando datos, columna espaniol
datos['sugerencia_es'] = datos['sugerencia_es'].str.replace('[,]','')

datos['sugerencia_es'] = datos['sugerencia_es'].apply(lambda x: elimina_tildes(x))
datos['sugerencia_es'].head()



#n-grams
datos['n-gram']=  datos['sugerencia_es'].apply(lambda x: TextBlob(x).ngrams(2))


def gestion_terminos(ngrams):
    lista_terminos = []
    for row in ngrams:
        lista_terminos.append("_".join(row))
    return lista_terminos

datos['terminos'] = datos["n-gram"].apply(lambda x: " ".join(gestion_terminos(x)))
datos[['cleaned','terminos']].head()

print datos['terminos']

#analisis de sentimiento y almacenando

#train['cleaned'][:5].apply(lambda x: TextBlob(x).sentiment)
datos['sentiment'] = datos['cleaned'].apply(lambda x: TextBlob(x).sentiment[0])
datos[['cleaned','sentiment']].head()




with open("datos_sentimientos.csv", 'wb') as csv_file:
    csv_file.write("id_movilidad,correo,sugerencia_es,sentiment_value,sentimiento,terminos\n")
    for i in range(len(datos['id_movilidad'])):
        sentimiento = "neutral"
        if datos['sentiment'][i]>0 : 
            sentimiento = "positivo"
        elif datos['sentiment'][i]<0 : 
            sentimiento = "negativo"
            


        lineresult = str(datos['id_movilidad'][i]) + "," + str(datos['correo'][i]) + "," + str(datos['sugerencia_es'][i]) + "," + str(datos['sentiment'][i]) + "," + sentimiento + "," + str(datos['terminos'][i])
        csv_file.write(lineresult + "\n")
#        print lineresult




