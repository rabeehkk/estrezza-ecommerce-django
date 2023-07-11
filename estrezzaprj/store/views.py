from django.shortcuts import render, get_object_or_404,HttpResponse
from .models import Product
from category.models import Category
from carts.models import *
from carts.views import _cart_id

# for OR operations in django
from django.db.models import Q


# paginator to do the next page links:
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator



# Create your views here.


# handling paginator here
def store(request, category_slug=None):
    
    # view to set url for different categories
    
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug= category_slug)
        products = Product.objects.filter(category= categories, is_available= True)
        # paginator
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        # 
        product_count = products.count()
    else:
        # saving all the items from products to list it in a dictionary
        products = Product.objects.all().filter(is_available=True).order_by('id')
        # taking product count
        
        # paginator to do the page 1,2,3...etc
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        # 
        product_count = products.count()
        
        
    
    context = {
        'products': paged_products,
        'product_count' : product_count,
        
    }
    return render(request,'store/store.html',context)

# for product detail page(single item)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug= category_slug, slug= product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id= _cart_id(request), product = single_product).exists()
        
            
    except Exception as e:
        raise e
    
    context= {
        'single_product': single_product,
        'in_cart' : in_cart,
    }
    
    
    return render(request, 'store/product_detail.html',context)
    
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword: #if keyword is not None
            products = Product.objects.order_by('created_date').filter(Q(description__icontains= keyword) |  Q(product_name__icontains=keyword)) # whats i contains? it will look for whole description and and if it find anything same like what we are checking it will filter(we are cheaacking keyword here and also the keyword is that we are getting from url)
                                               #' Q or Queryset is the way we bring in OR operation in django' , we are importing it
            product_count = products.count()
            
    context = {
        
        'products' : products,
        'product_count' : product_count,
    }

    return render(request, 'store/store.html', context)




