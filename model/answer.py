# -*- coding: utf-8 -*-
import numpy as np
from sentence_transformers import SentenceTransformer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import joblib
model = joblib.load('model/kmeans_model.pkl')

# Предварительная обработка текстов
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

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
transformer = SentenceTransformer('distilbert-base-nli-mean-tokens')

def get_cluster(text):
    prep_text = preprocess_text(text)
    embs = transformer.encode([prep_text])
    cluster = model.predict(embs)
    return cluster

