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
