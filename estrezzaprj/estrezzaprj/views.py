from django.http import HttpResponse
from django.shortcuts import render
from store.models import  Product


# my views

def home(request):
    products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products': products,
    }
    
    return render(request, 'home.html',context)

def userlogin(request):
    return render(request, 'userlogin.html')