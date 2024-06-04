# ml/models.py
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from django.conf import settings
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

class MLModels:
    @staticmethod
    def recommend_products(user_id):
        # Example collaborative filtering using user-item interaction matrix
        user_item_matrix = pd.DataFrame(settings.USER_ITEM_INTERACTIONS)
        user_index = user_item_matrix.index.get_loc(user_id)
        similarity_matrix = cosine_similarity(user_item_matrix)
        similar_users = similarity_matrix[user_index]
        
        # Get top N similar users
        similar_users_indices = similar_users.argsort()[-2:-11:-1]
        
        # Aggregate their top rated products
        recommended_products = []
        for index in similar_users_indices:
            top_products = user_item_matrix.iloc[index].sort_values(ascending=False).index.tolist()
            recommended_products.extend(top_products)
        
        # Return unique recommended products
        return list(set(recommended_products))

    @staticmethod
    def dynamic_pricing(product_id):
        # Example dynamic pricing based on demand and competition
        historical_data = pd.DataFrame(settings.HISTORICAL_PRICES)
        demand_data = pd.DataFrame(settings.DEMAND_DATA)
        
        current_demand = demand_data[demand_data['product_id'] == product_id]['demand'].values[0]
        competitor_prices = historical_data[historical_data['product_id'] == product_id]['competitor_price'].values
        
        base_price = np.mean(competitor_prices)
        dynamic_price = base_price * (1 + (current_demand / 100))
        
        return round(dynamic_price, 2)

    @staticmethod
    def customer_segmentation():
        # Example using KMeans clustering
        data = pd.DataFrame(settings.CUSTOMER_DATA)
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        kmeans = KMeans(n_clusters=5)
        segments = kmeans.fit_predict(data_scaled)
        return segments.tolist()

    @staticmethod
    def churn_prediction():
        # Example using logistic regression
        data = pd.DataFrame(settings.CUSTOMER_FEATURES)
        target = settings.CUSTOMER_CHURN_TARGET
        model = LogisticRegression()
        model.fit(data, target)
        predictions = model.predict(data)
        return predictions.tolist()

    @staticmethod
    def fraud_detection(transaction):
        # Example using isolation forest
        data = pd.DataFrame(settings.TRANSACTION_DATA)
        model = IsolationForest(contamination=0.01)
        model.fit(data)
        transaction_df = pd.DataFrame([transaction])
        fraud_score = model.predict(transaction_df)
        return fraud_score[0] == -1

    @staticmethod
    def sentiment_analysis(review):
        # Example using TfidfVectorizer and cosine similarity
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(settings.REVIEWS)
        review_vec = vectorizer.transform([review])
        sentiment_scores = cosine_similarity(review_vec, tfidf_matrix).flatten()
        avg_sentiment = np.mean(sentiment_scores)
        return "positive" if avg_sentiment > 0.5 else "negative"

    @staticmethod
    def forecast_demand():
        # Example using time series analysis with simple linear regression
        demand_data = pd.DataFrame(settings.DEMAND_DATA)
        demand_data['date'] = pd.to_datetime(demand_data['date'])
        demand_data.set_index('date', inplace=True)
        demand_series = demand_data['demand']
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, activation='relu', input_shape=(1,)),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        
        x = np.arange(len(demand_series)).reshape(-1, 1)
        y = demand_series.values
        
        model.fit(x, y, epochs=100, verbose=0)
        
        future = np.arange(len(demand_series), len(demand_series) + 10).reshape(-1, 1)
        forecast = model.predict(future)
        
        return forecast.flatten().tolist()

    @staticmethod
    def understand_query(query):
        # Example using a simple NLP model (like TfidfVectorizer)
        vectorizer = TfidfVectorizer()
        query_vec = vectorizer.fit_transform([query])
        features = vectorizer.get_feature_names_out()
        
        important_keywords = [features[i] for i in query_vec.toarray()[0].argsort()[-2:][::-1]]
        return important_keywords

    @staticmethod
    def image_search(image):
        # Example placeholder for image-based search using pre-trained CNN model
        # Here we use a dummy pre-trained model (like VGG16 or ResNet) for feature extraction
        model = tf.keras.applications.VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        image_features = model.predict(image)

        # Placeholder for comparing features with a database of product images
        # For simplicity, return a dummy list of products
        return ["product1", "product2"]

