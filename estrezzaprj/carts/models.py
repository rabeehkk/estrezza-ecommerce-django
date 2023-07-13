from django.db import models
from store.models import Product,Variation
from accounts.models import *

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank = True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    
    user = models.ForeignKey(Account, on_delete= models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True) #we can have same product with different variations in cart, so using many to many field to handle it
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null= True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    
    def sub_total(self):
        return self.product.price * self.quantity
    

    def __unicode__(self):
        return self.product
    