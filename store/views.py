from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order, OrderItem, Review, Wishlist
from .forms import ReviewForm
from django.urls import reverse

# Fetch the first two products
def index(request):
    products = Product.objects.all()[:4]
    return render(request, 'store/index.html', {'products': products})

# Display the product list
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# Display product details
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'store/product_detail.html', {'product': product, 'reviews': reviews})

# Add product to wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.product.add(product)
    return redirect('wishlist_detail')

# Display wishlist details
@login_required
def wishlist_detail(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'store/wishlist_detail.html', {'wishlist': wishlist})

# Remove product from wishlist
@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist_detail')

# Display cart
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    order, created = Order.objects.get_or_create(user=request.user, status='pending', defaults={'total_price': total_price})
    if not created:
        order.total_price = total_price
        order.save()
    
    return render(request, 'store/cart_detail.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price, 'order': order})

# Add product to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

# Update cart item quantity
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    action = request.GET.get('action')
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return JsonResponse({'quantity': cart_item.quantity, 'total_price': cart_item.total_price})

# Remove cart item
def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return JsonResponse({'success': True})

# Checkout process
@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    # Calculate the total price for each item and the subtotal
    for item in order_items:
        item.total_price = item.product.price * item.quantity

    subtotal = sum(item.total_price for item in order_items)
    shipping = 100  # example shipping cost
    total_price = subtotal + shipping

    # Update order total price
    order.total_price = total_price
    order.save()

    if request.method == 'POST':
        # Process the checkout form data here
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2', '')
        country = request.POST.get('country')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        # Additional shipping address and payment processing can be handled here

        # Redirect to order confirmation or another page
        return redirect('order_history')

    return render(request, 'store/checkout.html', {
        'order': order,
        'order_items': order_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total_price': total_price
    })


# Order history
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_history.html', {'orders': orders})

# Order detail
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'store/order_detail.html', {'order': order, 'order_items': order_items})

# Add a product review
@login_required
def leave_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'store/leave_review.html', {'form': form, 'product': product})

# Search products
def search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'store/product_list.html', {'query': query, 'results': results})

# Add product (admin)
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm

@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})


# add to wishlist
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Wishlist

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.product.add(product)
    return redirect('wishlist_detail')

@login_required
def wishlist_detail(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.product.all()
    return render(request, 'store/wishlist_detail.html', {'wishlist': wishlist, 'products': products})

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.product.remove(product)
    return redirect('wishlist_detail')





# machine learning implementation
# ecommerce/views.py
import requests
import logging
from django.conf import settings
from django.shortcuts import render
from .models import Product

logger = logging.getLogger(__name__)

def get_recommendations(user_id):
    try:
        response = requests.get(f"{settings.ML_API_URL}/recommend_products/{user_id}/")
        response.raise_for_status()  # Raise an error for bad status codes
        recommendations = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching recommendations: {e}")
        recommendations = []
    except ValueError as e:
        logger.error(f"Error decoding JSON response: {e}")
        logger.error(f"Response content: {response.content}")
        recommendations = []
    return recommendations

def product_list(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        recommendations = get_recommendations(request.user.id)
        recommended_products = Product.objects.filter(id__in=recommendations)
    else:
        recommended_products = []
    return render(request, 'store/product_list.html', {'products': products, 'recommended_products': recommended_products})


# search functionality

# store/views.py
from django.shortcuts import render
from .models import Product

def search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'store/product_list.html', {'query': query, 'results': results})


# machine learning part
# ecommerce/views.py
import requests
import logging
from django.conf import settings
from django.shortcuts import render
from .models import Product

logger = logging.getLogger(__name__)

def _make_ml_request(url, method="GET", data=None):
    try:
        if method == "POST":
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error with ML API request: {e}")
        return {}
    except ValueError as e:
        logger.error(f"Error decoding JSON response: {e}")
        return {}

def get_recommendations(user_id):
    return _make_ml_request(f"{settings.ML_API_URL}/recommend_products/{user_id}/") or []

def get_dynamic_pricing(product_id):
    return _make_ml_request(f"{settings.ML_API_URL}/dynamic_pricing/{product_id}/")

def get_customer_segments():
    return _make_ml_request(f"{settings.ML_API_URL}/customer_segmentation/")

def get_churn_predictions():
    return _make_ml_request(f"{settings.ML_API_URL}/churn_prediction/")

def detect_fraud(transaction):
    return _make_ml_request(f"{settings.ML_API_URL}/fraud_detection/", method="POST", data=transaction)

def analyze_sentiment(review):
    return _make_ml_request(f"{settings.ML_API_URL}/sentiment_analysis/", method="POST", data={"review": review})

def get_demand_forecast():
    return _make_ml_request(f"{settings.ML_API_URL}/forecast_demand/")

def understand_user_query(query):
    return _make_ml_request(f"{settings.ML_API_URL}/understand_query/", method="POST", data={"query": query})

def image_based_search(image):
    return _make_ml_request(f"{settings.ML_API_URL}/image_search/", method="POST", data={"image": image})

def predict_customer_lifetime_value(customer_id):
    return _make_ml_request(f"{settings.ML_API_URL}/predict_clv/{customer_id}/")

def recommend_product_bundles(user_id):
    return _make_ml_request(f"{settings.ML_API_URL}/recommend_bundles/{user_id}/")

def personalize_email_content(user_id):
    return _make_ml_request(f"{settings.ML_API_URL}/personalize_email/{user_id}/")

def adaptive_search_ranking(query, user_id):
    return _make_ml_request(f"{settings.ML_API_URL}/adaptive_ranking/", method="POST", data={"query": query, "user_id": user_id})

def personalize_user_experience(user_id):
    return _make_ml_request(f"{settings.ML_API_URL}/personalize_experience/{user_id}/")

def recover_abandoned_cart(user_id):
    return _make_ml_request(f"{settings.ML_API_URL}/recover_abandoned_cart/{user_id}/")

def process_voice_search(voice_input):
    return _make_ml_request(f"{settings.ML_API_URL}/voice_search/", method="POST", data={"voice_input": voice_input})

def predict_trends():
    return _make_ml_request(f"{settings.ML_API_URL}/predict_trends/")

def chatbot_support(user_query):
    return _make_ml_request(f"{settings.ML_API_URL}/support_chatbot/", method="POST", data={"query": user_query})

def monitor_website_security():
    return _make_ml_request(f"{settings.ML_API_URL}/monitor_security/")

def analyze_user_behavior(user_id):
    return _make_ml_request(f"{settings.ML_API_URL}/analyze_behavior/{user_id}/")

def create_dynamic_landing_page(user_id):
    return _make_ml_request(f"{settings.ML_API_URL}/create_dynamic_page/{user_id}/")

def analyze_social_media_activity(user_id):
    return _make_ml_request(f"{settings.ML_API_URL}/analyze_social_media/{user_id}/")

def optimize_supply_chain():
    return _make_ml_request(f"{settings.ML_API_URL}/optimize_supply_chain/")

def fetch_analytics_dashboard():
    return _make_ml_request(f"{settings.ML_API_URL}/analytics_dashboard/")

def product_list(request):
    products = Product.objects.all()
    recommended_products = []
    
    if request.user.is_authenticated:
        recommendations = get_recommendations(request.user.id)
        if recommendations:
            recommended_products = Product.objects.filter(id__in=recommendations)
    
    context = {
        'products': products,
        'recommended_products': recommended_products,
        'dynamic_pricing': get_dynamic_pricing(request.GET.get('product_id')) or {},
        'customer_segments': get_customer_segments() or {},
        'churn_predictions': get_churn_predictions() or {},
        'fraud_detection': detect_fraud(request.POST) or {},
        'sentiment_analysis': analyze_sentiment(request.POST.get('review')) or {},
        'demand_forecast': get_demand_forecast() or {},
        'understood_query': understand_user_query(request.POST.get('query')) or {},
        'image_search_results': image_based_search(request.POST.get('image')) or {},
        'predicted_clv': predict_customer_lifetime_value(request.GET.get('customer_id')) or {},
        'bundled_recommendations': recommend_product_bundles(request.user.id) or {},
        'personalized_email': personalize_email_content(request.user.id) or {},
        'adaptive_ranking_results': adaptive_search_ranking(request.GET.get('query'), request.user.id) or {},
        'personalized_experience': personalize_user_experience(request.user.id) or {},
        'abandoned_cart_recovery': recover_abandoned_cart(request.user.id) or {},
        'voice_search_results': process_voice_search(request.POST.get('voice_input')) or {},
        'predicted_trends': predict_trends() or {},
        'chatbot_response': chatbot_support(request.POST.get('user_query')) or {},
        'security_alerts': monitor_website_security() or {},
        'user_behavior': analyze_user_behavior(request.user.id) or {},
        'dynamic_landing_page': create_dynamic_landing_page(request.user.id) or {},
        'social_media_analysis': analyze_social_media_activity(request.user.id) or {},
        'supply_chain_optimization': optimize_supply_chain() or {},
        'real_time_analytics': fetch_analytics_dashboard() or {},
    }
    
    return render(request, 'store/product_list.html', context)
