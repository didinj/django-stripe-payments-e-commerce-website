from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def formatted_price(self):
        return f"${self.price:.2f}"
    
class Order(models.Model):
    session_id = models.CharField(max_length=255)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.email}"
