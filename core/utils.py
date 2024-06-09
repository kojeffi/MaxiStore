import pandas as pd
from sklearn.neighbors import NearestNeighbors
from .models import Cart, Product

def get_recommendations(user_id, n_recommendations=5):
    carts = Cart.objects.all()
    data = {
        'user_id': [cart.user.id for cart in carts],
        'product_id': [cart.product.id for cart in carts],
        'quantity': [cart.quantity for cart in carts]
    }
    df = pd.DataFrame(data)
    
    user_product_matrix = df.pivot_table(index='user_id', columns='product_id', values='quantity', fill_value=0)
    
    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(user_product_matrix)
    
    user_index = user_product_matrix.index.tolist().index(user_id)
    
    distances, indices = model.kneighbors([user_product_matrix.iloc[user_index]], n_neighbors=n_recommendations+1)
    
    similar_users = [user_product_matrix.index[i] for i in indices.flatten() if i != user_index]
    
    recommendations = []
    for user in similar_users:
        user_products = df[df['user_id'] == user]['product_id'].tolist()
        recommendations.extend(user_products)
    
    recommended_product_ids = pd.Series(recommendations).value_counts().index.tolist()
    
    recommended_products = Product.objects.filter(id__in=recommended_product_ids[:n_recommendations])
    
    return recommended_products
