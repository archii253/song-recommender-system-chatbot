# train_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from config import Config

# This would use a dataset of songs with descriptions/tags
# For demonstration, we'll create a dummy dataset
data = {
    'artist': ['The Beatles', 'Radiohead', 'Daft Punk', 'Kendrick Lamar', 'Taylor Swift'],
    'track': ['Yesterday', 'Paranoid Android', 'Get Lucky', 'HUMBLE.', 'Blank Space'],
    'description': [
        'Classic melancholic ballad by the Beatles',
        'Experimental rock song with complex structure',
        'Funky disco-influenced electronic track',
        'Hard-hitting hip-hop with social commentary',
        'Pop anthem about love and relationships'
    ]
}

df = pd.DataFrame(data)

# Create combined text for vectorization
df['combined'] = df['artist'] + ' ' + df['track'] + ' ' + df['description']

# Vectorize text
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['combined'])

# Compute similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Save model
with open(Config.SIMILARITY_MODEL_PATH, 'wb') as f:
    pickle.dump({
        'vectorizer': vectorizer,
        'similarity_matrix': cosine_sim,
        'tracks': df[['artist', 'track']].to_dict('records')
    }, f)

print("Model trained and saved successfully!")