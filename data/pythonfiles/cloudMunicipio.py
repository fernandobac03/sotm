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
import matplotlib.pyplot as plt



datos = pd.read_csv('twitter_analisis_sentimiento_todo2019_full.csv')


datos['fecha']=  datos['creado'].apply(lambda x: x.split()[0])
datos[['creado', 'fecha']].head()
datos = datos.sort_values(['fecha'], ascending=[True])

datos['hora']=  datos['creado'].apply(lambda x: x.split()[1])
datos[['creado', 'hora']].head()


datos['mes']=datos['fecha'].apply(lambda x: x.split('-')[1])
datos[['fecha', 'mes']].head()

datos_pos = datos[ datos['polaridad'] == 'positivo']
datos_pos = datos_pos.sort_values(['fecha'], ascending=[True])
try:
    datos_cloud_pos = datos_pos['texto_es']
except: 
    print "Error: no se ha podido graficar la nube de positivos"




datos_neg = datos[ datos['polaridad'] == 'negativo']
datos_neg = datos_neg.sort_values(['fecha'], ascending=[True])
try:
    datos_cloud_neg = datos_neg['texto_es']
except: 
    print "Error: no se ha podido graficar la nube de negativos"



datos_plot_pos = datos_pos['valor_polaridad']
datos_plot_neg = datos_neg['valor_polaridad']
#dibujar x-y positivos y negativos
plt.plot(datos_plot_pos, 'g^', datos_plot_neg, 'rs')
#plt.set_title(title)
#    ax.set_xlabel(x_label)
#    ax.set_ylabel(y_label)
#plt.axis([0, 200, -1, 2])
#plt.show()
datos_pos = datos_pos.sort_values(['fecha','hora'], ascending=[True, True])
datos_neg = datos_neg.sort_values(['fecha','hora'], ascending=[True, True])
print datos_pos['creado']

print datos_neg['creado']
fig, ax_a = plt.subplots()
for polaridad in ['positivo', 'negativo']:
    n = 750
    #scale = 200.0 * np.random.rand(n)
    scale = 50
    transparencia = 0.4
    if (polaridad=='positivo'):
        ax_a.plot(datos_pos['fecha'], datos_pos['valor_polaridad'], c='tab:green',label=polaridad,
               alpha=transparencia)
   # if (polaridad=='negativo'):
   #     ax_a.plot(str(datos_neg['polaridad']), datos_neg['valor_polaridad'], c='tab:red', s=scale, label=polaridad,
     #          alpha=transparencia, edgecolors='none')#


#ax.legend()
ax_a.grid(False)
   




fig, ax = plt.subplots()
for polaridad in ['positivo', 'negativo']:
    n = 750
    #scale = 200.0 * np.random.rand(n)
    scale = 50
    transparencia = 0.4
    if (polaridad=='positivo'):
        ax.scatter(datos_pos['fecha'], datos_pos['valor_polaridad'], c='tab:green', s=scale, label=polaridad,
               alpha=transparencia, edgecolors='none')
    if (polaridad=='negativo'):
        ax.scatter(datos_neg['fecha'], datos_neg['valor_polaridad'], c='tab:red', s=scale, label=polaridad,
               alpha=transparencia, edgecolors='none')


ax.legend()
ax.grid(False)

#plt.show()



datos = datos.sort_values(['fecha'], ascending=[True])
fecha_analizada = datos['fecha'][0]
total_elementos =len(datos['fecha']) 
tendencia = []
sumapos=0.0
subelementopos = 0
sumaneg=0.0   
subelementoneg = 0 
promediopos = 0
promedioneg = 0

print datos['fecha']
for i in range(0,total_elementos):
    if (datos['fecha'][i] == fecha_analizada):
        if (datos['polaridad'][i]=='positivo'):
            subelementopos = subelementopos + 1
            sumapos=sumapos+datos['valor_polaridad'][i]
        if (datos['polaridad'][i]=='negativo'):
            subelementoneg = subelementoneg + 1
            sumaneg=sumaneg+datos['valor_polaridad'][i]      
    else:
        if subelementopos>0:
            promediopos = sumapos/subelementopos
        if subelementoneg>0:
            promedioneg = sumaneg/subelementoneg
        tendencia.append([fecha_analizada, promediopos, promedioneg])
        fecha_analizada = datos['fecha'][i] 
        subelementopos = 0 
        sumapos=0   
        subelementoneg = 0 
        sumaneg=0   
        if (datos['polaridad'][i]=='positivo'):
            subelementopos = subelementopos + 1
            sumapos=sumapos+datos['valor_polaridad'][i]
        if (datos['polaridad'][i]=='negativo'):
            subelementoneg = subelementoneg + 1
            sumaneg=sumaneg+datos['valor_polaridad'][i]    

datos_tendencia = pd.DataFrame(data=tendencia, 
                    columns=['fecha', 'promedio_polaridad_pos', 'promedio_polaridad_neg']) 
datos_tendencia = datos_tendencia.sort_values(['fecha'], ascending=[True])
datos_tendencia = datos_tendencia.drop_duplicates(datos_tendencia.columns[~datos_tendencia.columns.isin(['fecha'])],
                        keep='first')
print datos_tendencia

def lineplot(x_data, y_data, x_label="", y_label="", title=""):
    # Create the plot object
    _, ax = plt.subplots()

    # Plot the best fit line, set the linewidth (lw), color and
    # transparency (alpha) of the line
    ax.plot(x_data, y_data, lw = 2, color = '#539caf', alpha = 1)

    # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()


lineplot(datos_tendencia['fecha'], datos_tendencia['promedio_polaridad_pos'])


#dibujar nube de palaras

stopwordsList = stopwords.words('spanish')
newStopWords = ['alcalde','cuenca','pedro','palacios','est','sr','ser','solo','ciudad','gesti','si','as','tambi','cuencaunida','ah','hace','ya_que','a_los','que_se',
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
#wordcloud_draw(datos_cloud_pos,'white')
print("Negative words")
#wordcloud_draw(datos_cloud_neg)


#print train_pos
#print train
