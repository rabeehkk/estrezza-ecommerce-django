from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from category.models import Category
from accounts.models import Account
from store.models import Product
from django.contrib import messages

# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_superadmin:
            login(request, user)
            return redirect('admin_dashboard')  # Replace 'admin_dashboard' with the appropriate URL for your admin dashboard
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('admin_login')
    else:
        message = ''

    context = {'message': message}
    return render(request, 'adminside/admin_login.html', context)


def admin_logout(request):
    logout(request)
    return redirect('admin_login')  # Redirect to the admin login page after logging out

@login_required(login_url='admin_login')
def block_user(request,id):
    account = Account.objects.get(pk = id)
    account.is_active = False
    account.save()
    return redirect('admin_user')

@login_required(login_url='admin_login')
def unblock_user(request,id):
    account = Account.objects.get(pk = id)
    account.is_active = True
    account.save()
    return redirect('admin_user')


# dashboard:
@login_required(login_url='admin_login')
def admin_dashboard(request):
    return render(request, 'adminside/admin_dashboard.html')

# list users, categories and products:
@login_required(login_url='admin_login')
def admin_user(request):
    account_object= Account.objects.all
    context ={
        'account_object': account_object
    }
    return render(request, 'adminside/admin_user.html',context)

@login_required(login_url='admin_login')
def admin_product(request):
    product_object = Product.objects.all
    context = {
        'product_object': product_object
    }
    return render(request, 'adminside/admin_product.html',context)

@login_required(login_url='admin_login')
def admin_category(request):
    category_object = Category.objects.all
    context = {
        'category_object': category_object
    }
    return render(request, 'adminside/admin_category.html', context)


# category actions: add,delete,edit
@login_required(login_url='admin_login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.slug = slugify(category.category_name)
            category.save()
            messages.success(request, 'Category added successfuly.')
            return redirect('admin_category')
        
    else:
        form = CategoryForm()
    context = {
        'form': form
    }
        
    
    return render(request, 'adminside/add_category.html',context )


@login_required(login_url='admin_login')
def delete_category(request,id):
    category = Category.objects.get(pk=id)
    category.delete()
    messages.warning(request, 'Category deleted')
    return redirect('admin_category')

@login_required(login_url='admin_login')
def edit_category(request, id):
    category = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category edited successfully')
            return redirect('admin_category')
    else:
        form = CategoryForm(instance=category)

    context = {
        "form": form
    }
    return render(request, 'adminside/edit_category.html', context)

# products actions: (add,delete,edit):
@login_required(login_url='admin_login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.slug = slugify(product.product_name)
            product.category_id = request.POST.get('category')  # Retrieve the selected category ID   
            product.save()
            messages.success(request, 'Product added successfuly.')
            return redirect('admin_product')  # Redirect to the admin product page after saving

    else:
        form = ProductForm()
        categories = Category.objects.all
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'adminside/add_product.html', context)

@login_required(login_url='admin_login')
def delete_product(request,id):
    product = Product.objects.get(pk=id)
    product.delete()
    messages.warning(request, 'Product deleted')
    return redirect('admin_product')

@login_required(login_url='admin_login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product edited successfully')
            return redirect('admin_product')
    else:
        form = ProductForm(instance=product)

    context = {
        "form": form
    }
    return render(request, 'adminside/edit_product.html', context)