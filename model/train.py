# -*- coding: utf-8 -*-

import pandas as pd
from sentence_transformers import SentenceTransformer
import scipy.spatial
import nltk
import subprocess
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import joblib

df = pd.read_json('dataset_hack.json')

# Download and unzip wordnet
'''
try:
    nltk.data.find('wordnet.zip', paths=['/custom/path/to/nltk_data'])
except:
    nltk.download('wordnet')
    command = "unzip /corpora/wordnet.zip -d /corpora"
    subprocess.run(command.split())
    nltk.data.path.append('')
'''

stop_words = set(stopwords.words('russian'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Токенизация
    tokens = word_tokenize(text)
    # Удаление стоп-слов
    tokens = [token for token in tokens if token.lower() not in stop_words]
    # Лемматизация
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # Объединение токенов обратно в строку
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

# Загрузка предобученной модели DistilBERT
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

# Пример текстов
texts = df['message']

# Преобразование и предварительная обработка текстов
preprocessed_texts = [preprocess_text(text) for text in texts]

# Преобразование текстов в эмбеддинги
embeddings = model.encode(preprocessed_texts)

from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

# Перебор количества кластеров
'''
max_clusters = 24
inertias = []
for num_clusters in range(1, max_clusters + 1):
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(embeddings)
    inertias.append(kmeans.inertia_)

# Визуализация метода локтя
plt.plot(range(1, max_clusters + 1), inertias, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal Cluster Number')
plt.show()
'''

'''
clusters = kmeans.labels_
# Вывод текстов в каждом кластере
for cluster_id in range(num_clusters):
    cluster_texts = [texts[i] for i, cluster_label in enumerate(clusters) if cluster_label == cluster_id]
    print(f"Cluster {cluster_id}:")
    for text in cluster_texts:
        print(text)
    print()
'''

kmeans = KMeans(n_clusters=24)
kmeans.fit(embeddings)

joblib.dump(kmeans, 'kmeans_model.pkl')

