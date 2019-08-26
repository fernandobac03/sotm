# coding=utf-8
from nltk.corpus import stopwords
from textblob import TextBlob
import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import requests
#from translate import traducir
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
import unicodedata 
import json
import tweepy as tw
import re
from unicodedata import normalize
from progress.bar import Bar, ChargingBar

from googletrans import Translator

import goslate
#from translate import Translator
from yandex.Translater import Translater


#example: https://www.earthdatascience.org/courses/earth-analytics-python/using-apis-natural-language-processing-twitter/get-and-use-twitter-data-in-python/
consumer_key= 'VDaBPHvkNh9JEj3vzDzSiJuRd'
consumer_secret= 'R22tbJSTwE0eqCP3HNUe8WbIm2E43Xsg2yBmQjTHkO9xPmDPK7'
access_token= '144021815-NkO6eA02sNKXmlCY7lVwN26FK0DtSVTUJGjLFRsx'
access_token_secret= 'oMkLLs0wW9QLMXyWMwP0K8Gs7vsfNPBRbBij7G5JEHeJw'


def eliminar_emoticones(texto):
    texto = re.sub(r'([^\s\w\@]|_)+', '', texto)    
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    return texto
def eliminar_caracteres_raros(texto):
    texto = texto.encode('utf-8')
    texto = re.sub('[!,#$]', '', texto)   

    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    texto = emoji_pattern.sub(r'', texto) # no emoji
    return texto





def conexion_twitter():
    print "conectando a twitter"
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tw.API(auth, wait_on_rate_limit=True)

def twitear_twitter():
    api = conexion_twitter()    
    api.update_status("Test from ldapp")
#twitear_twitter()

def traduciendo(text):
    #traduciendo a ingles
    text = eliminar_emoticones(text)
    translator = Translator()    
    try:
        text = translator.translate(text, dest='en',).text         
    except:
        print 'no se pudo traducir: ' + text
    return text


    #tr = Translater()
    #tr.set_key('trnsl.1.1.20190816T201419Z.dc11d7843f127ee3.78b742b581ef4c56154b082b1ef14a6abf5db303') # Api key found on https://translate.yandex.com/developers/keys
    #tr.set_from_lang('es')
    #tr.set_to_lang('en')
    #text = eliminar_caracteres_raros(text)
    #tr.set_text(str(text))
    #text = tr.translate()
    #return text

#    translator= Translator(to_lang='it')
#    text = translator.translate("hola mundo, buen dia")
#    print text
#    return text

#    gs = goslate.Goslate()
#    return gs.translate(text, 'en')

def search_twitter(search_words, date_since, elementos):
    api = conexion_twitter()    
    tweets = tw.Cursor(api.search,
              q=search_words,
              lang="es",
              since=date_since,
              tweet_mode="extended").items(elementos)
    return tweets
def recuperar_twitter():
    search_words = ["@pedropalaciosu", "Alcalde de Cuenca", "Pedro Palacios"]
    #search_words = "#TestUC"
    date_since = "2019-01-01"
    # Collect tweets
    tweets = []
    for termino in search_words:
        tweets.extend(search_twitter(termino + " -filter:retweets", date_since, 100000))

    # Iterate on tweets
    all_tweets_aux = []
    numero_de_tweet_procesado = 0;
    total_tweets = len(tweets)
    bar1 = Bar('Procesando:', max=total_tweets)
    
    for tweet in tweets:
  
        bar1.next()
        ##print("test: " + str(json.dumps(tweet._json)))
        #print("creacion: " + str(tweet.created_at))
        #print("Tweet: " + str(tweet))
        #print("Usuario: "  + tweet.user.name )
        #print("usuario - Localizacion: " +  tweet.user.location ) 
        #print("usuario - description: " +  tweet.user.description ) 
        #print("usuario - seguidores: " +  str(tweet.user.followers_count) ) 
        texto = ""
        try:
            texto = tweet.full_text.lower()
        except:
            print "problemas en recuperar full text en: " + tweet 

        #eliminando terminos
        terminosEliminar = ["alcalde de cuenca"] 
        for termino in terminosEliminar:
            texto = texto.replace(termino, "")         

        #eliminando stopwords
        stopwordsU = stopwords.words('spanish')
        newStopWords = ['cuenca', 'alcade']
        stopwordsU.extend(newStopWords)        
        texto =  " ".join(texto for texto in texto.split() if texto not in newStopWords)
        
        #eliminando etiquetas @
        texto = " ".join(texto for texto in texto.split() if "@" not in texto )
        #eliminando urls
        texto = " ".join(texto for texto in texto.split() if "http" not in texto )
        
        texto_en = eliminar_caracteres_raros(eliminar_emoticones(traduciendo(texto)))
        texto_limpio =  eliminar_caracteres_raros(texto)

            
       
        all_tweets_aux.append([tweet.created_at, texto_limpio, texto_en, tweet.user.name, tweet.user.location, tweet.user.description, tweet.user.followers_count])


    all_tweets = pd.DataFrame(data=all_tweets_aux, 
                    columns=['creado', 'texto_es', 'texto_en', 'usuario', 'ubicacion_usuario', 'descripcion_usuario', 'seguidores_usuario'])
    bar1.finish()
        
    return all_tweets


def corregir_texto(texto):
    return eliminar_caracteres_raros(eliminar_emoticones(str(texto))).replace(",", "").replace('"','') 


def obteniendo_ngrams(texto, numero):
    valor = []
    try:
        valor = TextBlob(corregir_texto(texto)).ngrams(numero)
    except Exception as e:
        print ('Error n-grams en: ' + texto)        
        print e
    return valor

def gestion_terminos(ngrams):
    lista_terminos = []
    for row in ngrams:
        lista_terminos.append("_".join(row))
    return lista_terminos

def obteniendo_sentimiento(texto):
    polarity = 0.0
    try:
        polarity = TextBlob(texto).sentiment.polarity
    except:
        print ('Error en: ' + texto)
    return polarity
   
def preprocesar_twitter():
    all_tweets = recuperar_twitter()
  
    datos = all_tweets

    #datos['total_palabras'] = datos['texto_es'].apply(lambda x: len(str(x).split(" ")))
    #datos[['texto_es', 'total_palabras']].head()

    ##a minusculas    
    #datos['texto_minusculas'] = datos['texto'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    #datos[['texto', 'texto_minusculas']].head()
    
    ##eliminando etiquetas y url
    #datos['texto_sin_etiquetas_urls'] = datos['texto_en'].apply(lambda x: " ".join(x for x in x.split() if "@" not in x ))
    #datos['texto_sin_etiquetas_urls'] = datos['texto_sin_etiquetas_urls'].apply(lambda x: " ".join(x for x in x.split() if "http" not in x ))
    #datos[['texto_en', 'texto_sin_etiquetas_urls']].head()


    
    
    #traduciendo
    #datos['texto_ingles'] = datos['texto_sin_etiquetas_urls'].apply(lambda x: traduciendo(x))
   

    #datos['texto_ingles'] = datos['texto_sin_etiquetas_urls'].apply(lambda x: TextBlob(x).translate(to='en')) 
    #datos['texto_ingles'] = datos['texto_sin_etiquetas_urls'].apply(lambda x: x) 
    #datos[['texto_sin_etiquetas_urls' , 'texto_ingles']].head()
    
    #eliminando stopwords
    ##new_stopwords = set(stopwords.words('es')) - {'me', 'se', 'mas', 'deberia', 'deberian'}
    #stop = stopwords.words('english')
    #datos['texto_sin_stopwords'] = datos['texto_en'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    #datos[['texto_en', 'texto_sin_stopwords']].head()
    
    
    ##eliminando palabras raras
    #freq = pd.Series(' '.join(datos['cleaned']).split()).value_counts()[-10:]
    #freq = list(freq.index)
    #datos['cleaned'] = datos['cleaned'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
    #datos[['sugerencia_en', 'cleaned']].head()


    #ortografia - corrige texto en ingles
    #datos['texto_sin_stopwords'] = datos['texto_sin_stopwords'].apply(lambda x: str(TextBlob(x).correct()))
    #datos['texto_sin_stopwords'].head()
    #print datos['texto_sin_stopwords']
    #print datos['texto_mejor_ortografia']
    ##stemming , eliminando  terminaciones de palabras ing, ly, etc. no se si trabaja para espaniol
    ##st = PorterStemmer()
    ##train['stemming'] = train['cleaned'].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))
    ##train[['cleaned','stemming']].head()


    ##limpiando datos, columna espaniol
    #datos['sugerencia_es'] = datos['sugerencia_es'].str.replace('[,]','')

    #datos['sugerencia_es'] = datos['sugerencia_es'].apply(lambda x: elimina_tildes(x))
    #datos['sugerencia_es'].head()



    ##n-grams-2
    datos['n-gram-2']=  datos['texto_es'].apply(lambda x: obteniendo_ngrams(x, 2))
    datos['terminos_2'] = datos["n-gram-2"].apply(lambda x: " ".join(gestion_terminos(x)))
    datos[['texto_es','terminos_2']].head()
    #analisis de sentimiento y almacenando

    datos['n-gram-3']=  datos['texto_es'].apply(lambda x: obteniendo_ngrams(x, 3))
    datos['terminos_3'] = datos["n-gram-3"].apply(lambda x: " ".join(gestion_terminos(x)))
    datos[['texto_es','terminos_3']].head()
    #analisis de sentimiento y almacenando

   
    #train['cleaned'][:5].apply(lambda x: TextBlob(x).sentiment)

    print datos['texto_en']

    datos['sentimiento'] = datos['texto_en'].apply(lambda x: obteniendo_sentimiento(x))
    datos[['texto_en','sentimiento']].head()

##link de analisis de sentimiento: https://medium.com/@himanshu_23732/sentiment-analysis-with-textblob-6bc2eb9ec4ab

    
    print "Total Tweets recuperados: " + str(len(datos['texto_es'])) 
    tweets_guardados = 0
    with open("twitter_analisis_sentimiento_todo2019_full_2.csv", 'wb') as csv_file:
        #csv_file.write("id_movilidad,correo,sugerencia_es,sentiment_value,sentimiento,terminos\n")
        csv_file.write("creado,texto_es,texto_en,polaridad,valor_polaridad,ubicacion_usuario,terminos_2, terminos_3\n")
    
        for i in range(len(datos['texto_es'])):
            polaridad = "neutral"
            if datos['sentimiento'][i]>0 : 
                polaridad = "positivo"
            elif datos['sentimiento'][i]<0 : 
                polaridad = "negativo"
            lineaImprimir = ""
            try: 
                lineaImprimir = str(str(datos['creado'][i]) + "," + datos['texto_es'][i] + "," + datos['texto_en'][i] + "," + polaridad + "," + str(datos['sentimiento'][i]) + "," + corregir_texto(str(datos['ubicacion_usuario'][i])) +","+ str(datos['terminos_2'][i]) +","+ str(datos['terminos_3'][i]))
            except:
                print "Error en lineaImprimir = ...  de: " + datos['texto_es'][i]
            else:
                try: 
                    csv_file.write(lineaImprimir + "\n")
                    tweets_guardados = i+1        
                except  Exception as e:
                    try: 
                        csv_file.write(corregir_texto(lineaImprimir) + "\n")
                    except  Exception as e:
                        print "Error: Segundo fallo en: No se ha guardado en archivo, tweet: " + datos['texto_es'][i]
                        print e
    #        print lineresult
    print "Total Tweets guardados: " + str(tweets_guardados)

preprocesar_twitter()








