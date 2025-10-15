from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    cart = Cart(request)
    cart.add(product_id=product_id)
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id=product_id)
    return redirect('cart_detail')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')
