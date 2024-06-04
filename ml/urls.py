from django.urls import path
from .views import (
    RecommendProducts, DynamicPricing, CustomerSegmentation, ChurnPrediction,
    FraudDetection, SentimentAnalysis, ForecastDemand, UnderstandQuery, ImageSearch
)

urlpatterns = [
    path('recommend_products/<int:user_id>/', RecommendProducts.as_view(), name='recommend_products'),
    path('dynamic_pricing/<int:product_id>/', DynamicPricing.as_view(), name='dynamic_pricing'),
    path('customer_segmentation/', CustomerSegmentation.as_view(), name='customer_segmentation'),
    path('churn_prediction/', ChurnPrediction.as_view(), name='churn_prediction'),
    path('fraud_detection/', FraudDetection.as_view(), name='fraud_detection'),
    path('sentiment_analysis/', SentimentAnalysis.as_view(), name='sentiment_analysis'),
    path('forecast_demand/', ForecastDemand.as_view(), name='forecast_demand'),
    path('understand_query/', UnderstandQuery.as_view(), name='understand_query'),
    path('image_search/', ImageSearch.as_view(), name='image_search'),
]
