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
import matplotlib.pyplot as plt



datos = pd.read_csv('datos_sentimientos.csv')

datos_pos = datos[ datos['sentimiento'] == 'positivo']
datos_cloud_pos = datos_pos['sugerencia_es']
datos_neg = datos[ datos['sentimiento'] == 'negativo']
datos_cloud_neg = datos_neg['sugerencia_es']

datos_plot_pos = datos_pos['sentiment_value']
datos_plot_neg = datos_neg['sentiment_value']
#dibujar x-y positivos y negativos
plt.plot(datos_plot_pos, 'g^', datos_plot_neg, 'rs')
#plt.axis([0, 200, -1, 2])
plt.show()


#dibujar nube de palaras

stopwordsList = stopwords.words('spanish')
newStopWords = ['a_la','de_la','de_lo','en_el','por_la','en_la','con_la','para_que','que_no','que_el','para_la','ya_que','a_los','que_se',
                          'en_el','me', 'se', 'mas', 'que_la', 'que_lo', 'a_las', 'para_los', 'que_es', 'y_que', 'de_que', 'de_las',
                           'en_las', 'y_de', 'lo_que', 'ya_sea', 'para_el', 'y_no' , 'en_las', 'deberia', 'deberian']
stopwordsList.extend(newStopWords)



def wordcloud_draw(data, color = 'black'):
    words = " ".join(data)
    cleaned_word = " ".join([word for word in words.split(" ")
                            if 'http' not in word
                                and not word.startswith('@')
                                and not word.startswith('#')
                                and word != 'RT'
                            ])
    wordcloud = WordCloud(stopwords=stopwordsList,
                      background_color=color,
                      width=2500,
                      height=2000,
                      normalize_plurals= True
                     ).generate(cleaned_word)
    plt.figure(1,figsize=(13, 13))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    
print("Positive words")
wordcloud_draw(datos_cloud_pos,'white')
print("Negative words")
#wordcloud_draw(datos_cloud_neg)


#print train_pos
#print train
