# %%
#Librerías básicas utiliadas
import numpy as np
import pandas as pd
import re
import os

#Librerías necesarias para abrir imágenes, generar nube de palabras y plot
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

#Librerías necesarias para la limpieza de datos
import string
import nltk
from nltk.corpus import stopwords

# %% ingestando datos parquet
#cargando df
df = pd.read_parquet("reviews_reviews_Automotive_5.gz.parquet", engine='pyarrow')


# %%
df = df['reviewText']
df = pd.DataFrame(df, columns=['reviewText'])

# %%
texto = []
for i in range(len(df)):
    row = df.iloc[i]['reviewText']
    texto.append(row)
    i = i+1

texto = " ".join(texto)


# %%
# Limpiar texto
texto = texto.lower()
texto = re.sub('\[.*?¿\]\%', ' ', texto)
texto = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto)
texto = re.sub('\w*\d\w*', '', texto)

# %%
# Eliminar stopwords 
stopwords = open("stopwords.txt", "r", encoding="utf8").read()

def eliminar_stopwords(texto, stopwords):
    return ' '.join([word for word in texto.split(' ') if word not in stopwords])

texto_final = eliminar_stopwords(texto, stopwords)

# %%
# WordCloud
# Import package
import matplotlib.pyplot as plt
# Import package stopwords
from wordcloud import WordCloud, STOPWORDS

# Define a function to plot word cloud
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud)
    # No axis details
    plt.axis("off")


# %%
#Generate Wordcloud
wordcloud = WordCloud(width=3000, height=2000, random_state=1, background_color='black',
                      colormap='Set2', collocations=False, stopwords=STOPWORDS).generate(texto_final)

# %%
#Generamos la carpeta 'imagenes'.
nueva_carpeta = 'images/'

try:
    os.mkdir(nueva_carpeta)

except OSError:
    print('Ya existe una carpeta llamada %s' % nueva_carpeta)
else:
    print('Se ha creado la carpeta: %s' % nueva_carpeta)

# Save image
wordcloud.to_file("images/wordcloud.png")



