
import json
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect


from .cart import Cart
from .forms import OrderForm
from .models import Category, Product, Order, OrderItem

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('cart_view')




def success(request):
    return render(request, 'store/success.html')

    
def change_quantity(request, product_id):
    action = request.GET.get('action', '')
    if action:
        quantity = 1 if action == 'increase' else -1
        cart = Cart(request)    
        cart.add(product_id, quantity, True)
    return redirect('cart_view')
    
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)
    return render(request, 'store/cart_view.html', {'cart': cart})

@login_required
def checkout(request):
    cart = Cart(request)

    if cart.get_total_cost() == 0:
        return redirect('cart_view')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            address = data.get('address', '')
            zipcode = data.get('zipcode', '')
            city = data.get('city', '')
            
            if first_name and last_name and address and zipcode and city:
                form = OrderForm(data)

                if not form.is_valid():
                    return JsonResponse({'error': 'Invalid form data'}, status=400)

                total_price = 0
                items = []

                for item in cart:
                    product = item['product']
                    total_price += product.price * int(item['quantity'])

                    items.append({
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': product.title
                            },
                            'unit_amount': int(product.price * 100),  # Amount in cents
                        },
                        'quantity': item['quantity']
                    })

                stripe.api_key = settings.STRIPE_SECRET_KEY 
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=items,
                    mode='payment',
                    success_url=f'{settings.WEBSITE_URL}cart/success/',
                    cancel_url=f'{settings.WEBSITE_URL}cart/',
                )

                payment_intent = session.id  # Use session.id for payment intent

                order = Order.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    zipcode=zipcode,
                    city=city,
                    created_by=request.user,
                    is_paid=True,
                    payment_intent=payment_intent,
                    paid_amount=total_price / 100  # Store amount in dollars
                )

                for item in cart:
                    product = item['product']
                    quantity = int(item['quantity'])
                    price = product.price * quantity

                    OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

                cart.clear()

                return JsonResponse({'session_id': session.id, 'order_id': order.id})
            else:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)
        except Exception as e:
            print(f"Error during checkout: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
        'pub_key': settings.STRIPE_PUB_KEY,
    })

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(
        title__icontains=query)
        |
        Q(description__icontains=query))
    
    return render(request, 'store/search.html', {
        'query': query,
        'products': products,})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)

    return render(request, 'store/category_detail.html',{
        'category': category,
        'products': products
    })

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    return render(request, 'store/product_detail.html', {'product': product})