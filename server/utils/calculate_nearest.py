import numpy as np
from scipy.spatial import cKDTree
import pandas as pd
import extcolors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def nearest_locations(data, latitude, longitude):
    df = pd.DataFrame(data)

    def find_k_nearest_neighbors_location(df, lat, lon, k=4):
        coordinates = df[['latitude', 'longitude']].to_numpy()
        tree = cKDTree(coordinates)
        distances, indices = tree.query(np.array([lat, lon]), k=k)
        return df.iloc[indices]

    target_latitude = latitude
    target_longitude = longitude

    result = find_k_nearest_neighbors_location(df, target_latitude, target_longitude)
    closest = []
    for entity in result['wikidata_id']:
        closest.append(entity)
    itself, first_closest, second_closest, third_closest = closest
    return first_closest, second_closest, third_closest

def nearest_color_cluster(data, id):
    df = pd.DataFrame(data)

    def find_k_nearest_neighbors_color(df, red, green, blue, k=3):
        colors = df[['red', 'green', 'blue']].to_numpy()
        tree = cKDTree(colors)
        distances, indices = tree.query(np.array([red, green, blue]), k=k)
        return df.iloc[indices]

    top,_ = extcolors.extract_from_path(f'{id}.jpg')
    red, green, blue = top[0][0]

    result = find_k_nearest_neighbors_color(df, red, green, blue, k=1)
    return result['color_cluster']

def nearest_text(data, description):
    df = pd.DataFrame(data)

    def cosine_similarity_for_one(df, target_description):
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(df['description'])
        
        # Transform the target description using the same vectorizer
        target_tfidf = vectorizer.transform([target_description])
        
        # Compute cosine similarity only for the target description
        cosine_similarities = cosine_similarity(target_tfidf, tfidf_matrix)
        
        return cosine_similarities

    def find_top3_similar_texts(df, target_description):
        cosine_similarities = cosine_similarity_for_one(df, target_description)
        
        # Get the indices of the top 3 similar descriptions (excluding the target description itself)
        top3_indices = cosine_similarities.argsort()[:, -4:-1][0][::-1]
        
        # Get the top 3 similar texts
        top3_similar_texts = df['description'].iloc[top3_indices].tolist()
        
        return top3_similar_texts

    top3_similar_texts = find_top3_similar_texts(df, description)

    top3 = []
    for text in top3_similar_texts:
        temp = df.loc[df['description'] == text]
        top3.append(temp['wikidata_id'].iloc[0])

    sim_text_one, sim_text_two, sim_text_three = top3
    return sim_text_one, sim_text_two, sim_text_three