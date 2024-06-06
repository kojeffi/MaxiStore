from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, Review, Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from .forms import ProductForm, ReviewForm
from .models import Cart, CartItem, Order, OrderItem
from django.utils import timezone

def index(request):
    # Fetch the first two products
    products = Product.objects.all()[:2]
    return render(request, 'store/index.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('wishlist_detail')

@login_required
def wishlist_detail(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'store/wishlist_detail.html', {'wishlist': wishlist})

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist_detail')

@login_required
def cart(request):
    cart = get_object_or_404(Cart, user=request.user, status='pending')
    return render(request, 'store/cart.html', {'cart': cart})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user, status='pending')
    order = Order.objects.create(user=request.user, total_price=sum(item.total_price for item in cart.cartitem_set.all()))
    for item in cart.cartitem_set.all():
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        item.product.stock -= item.quantity
        item.product.save()
    cart.cartitem_set.all().delete()
    return redirect('checkout_success')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'user_app/overview.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, status='pending')
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user, status='pending')
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart_detail.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price})

def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    action = request.GET.get('action')
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return JsonResponse({
        'quantity': cart_item.quantity,
        'total_price': cart_item.total_price
    })

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

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user, status='pending')
    order = Order.objects.create(user=request.user, total_price=sum(item.product.price * item.quantity for item in cart.cartitem_set.all()))
    for item in cart.cartitem_set.all():
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        item.product.stock -= item.quantity
        item.product.save()
    cart.cartitem_set.all().delete()
    return redirect('checkout')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'store/order_detail.html', {'order': order, 'order_items': order_items})

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
