from django.http import HttpResponse
from django.shortcuts import render,redirect
from store.models import  Product
from accounts.models import Account

from django.contrib.auth import authenticate


# my views

def home(request):
    products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products': products,
    }
    
    return render(request, 'home.html',context)
