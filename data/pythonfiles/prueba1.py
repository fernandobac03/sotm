
from nltk.corpus import stopwords
from textblob import TextBlob
import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import requests
from translate import traducir

#basico
train = pd.read_csv('/data/data/datos_en.csv')
train['word_count'] = train['sugerencia_movilidad'].apply(lambda x: len(str(x).split(" ")))
train[['sugerencia_movilidad', 'word_count']].head()

#eliminando stopwords
#new_stopwords = set(stopwords.words('es')) - {'me', 'se', 'mas', 'deberia', 'deberian'}
stop = stopwords.words('spanish')
train['cleaned'] = train['sugerencia_movilidad'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
train[['sugerencia_movilidad', 'cleaned']].head()

#eliminando palabras raras
freq = pd.Series(' '.join(train['cleaned']).split()).value_counts()[-10:]
freq = list(freq.index)
train['cleaned'] = train['cleaned'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
train[['sugerencia_movilidad', 'cleaned']].head()


#ortografia
#train['cleaned'] = train['cleaned'].apply(lambda x: str(TextBlob(x).correct()))
#train[['sugerencia_movilidad', 'cleaned']].head()

#stemming , eliminando  terminaciones de palabras ing, ly, etc. no se si trabaja para espaniol
#st = PorterStemmer()
#train['stemming'] = train['cleaned'].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))
#train[['cleaned','stemming']].head()

#analisis de sentimiento
#train['cleaned'][:5].apply(lambda x: TextBlob(x).sentiment)
train['sentiment'] = train['cleaned'].apply(lambda x: TextBlob(x).sentiment[0] )
train[['cleaned','sentiment']].head()


print train
