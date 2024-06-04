# ml/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MLModels

class RecommendProducts(APIView):
    def get(self, request, user_id, format=None):
        recommendations = MLModels.recommend_products(user_id)
        return Response(recommendations, status=status.HTTP_200_OK)

class DynamicPricing(APIView):
    def get(self, request, product_id, format=None):
        price = MLModels.dynamic_pricing(product_id)
        return Response({"price": price}, status=status.HTTP_200_OK)

class CustomerSegmentation(APIView):
    def get(self, request, format=None):
        segments = MLModels.customer_segmentation()
        return Response(segments, status=status.HTTP_200_OK)

class ChurnPrediction(APIView):
    def get(self, request, format=None):
        predictions = MLModels.churn_prediction()
        return Response(predictions, status=status.HTTP_200_OK)

class FraudDetection(APIView):
    def post(self, request, format=None):
        transaction = request.data
        is_fraud = MLModels.fraud_detection(transaction)
        return Response({"is_fraud": is_fraud}, status=status.HTTP_200_OK)

class SentimentAnalysis(APIView):
    def post(self, request, format=None):
        review = request.data.get("review")
        sentiment = MLModels.sentiment_analysis(review)
        return Response({"sentiment": sentiment}, status=status.HTTP_200_OK)

class ForecastDemand(APIView):
    def get(self, request, format=None):
        forecast = MLModels.forecast_demand()
        return Response(forecast, status=status.HTTP_200_OK)

class UnderstandQuery(APIView):
    def post(self, request, format=None):
        query = request.data.get("query")
        keywords = MLModels.understand_query(query)
        return Response(keywords, status=status.HTTP_200_OK)

class ImageSearch(APIView):
    def post(self, request, format=None):
        image = request.data.get("image")
        results = MLModels.image_search(image)
        return Response(results, status=status.HTTP_200_OK)

