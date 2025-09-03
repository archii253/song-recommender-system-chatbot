import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from config import Config

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

nlp = spacy.load('en_core_web_sm')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

class NLPProcessor:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.model = self.load_nlp_model()
    
    def load_nlp_model(self):
        try:
            return tf.keras.models.load_model(Config.NLP_MODEL_PATH)
        except:
            return None
    
    def preprocess_text(self, text):
        # Tokenization
        tokens = nltk.word_tokenize(text.lower())
        
        # Remove stopwords and lemmatize
        tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
        
        return ' '.join(tokens)
    
    def extract_entities(self, text):
        doc = nlp(text)
        entities = {
            'artists': [],
            'songs': [],
            'genres': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                entities['artists'].append(ent.text)
            elif ent.label_ == 'WORK_OF_ART':
                entities['songs'].append(ent.text)
        
        return entities
    
    def get_text_embedding(self, text):
        processed_text = self.preprocess_text(text)
        if self.model:
            sequence = self.tokenizer.texts_to_sequences([processed_text])
            padded = pad_sequences(sequence, maxlen=100)
            return self.model.predict(padded)[0]
        else:
            # Fallback to TF-IDF if model not available
            return self.vectorizer.fit_transform([processed_text]).toarray()[0]
    
    def calculate_similarity(self, text1, text2):
        embedding1 = self.get_text_embedding(text1)
        embedding2 = self.get_text_embedding(text2)
        return cosine_similarity([embedding1], [embedding2])[0][0]