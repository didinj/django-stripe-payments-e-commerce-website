from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product = Product.objects.get(id=product_id)
        product_id_str = str(product_id)

        if product_id_str not in self.cart:
            self.cart[product_id_str] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 0,
                'image': product.image.url if product.image else '',
            }
        self.cart[product_id_str]['quantity'] += quantity
        self.save()

    def remove(self, product_id):
        product_id_str = str(product_id)
        if product_id_str in self.cart:
            del self.cart[product_id_str]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
