from django.shortcuts import render,redirect
from . forms import *
from .models import *
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from . import verify
from carts.models import *
from carts.views import _cart_id
import requests

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # we dont have field in form to accept username or the field which allows the user to create a username, so instead we are creating a username ourselves from the email address they are  providing and splitting it at '@'
            username = email.split("@")[0]
            
            # user object:
                # inside the create user we will pass all the fields above
                # create_user() is from custom user model
                
            user = get_user_model().objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,

            )
            user.phone_number = phone_number
            user.save()
            auth.login(request, user)
            return redirect('home')
                   
            
    else:
        form = RegistrationForm()
            
    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.html',context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                # is_cart_item_exits returns a true or false value, by checking if the same cart item is there or not
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    # getting product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    
                    #  no we will get cart items from user to access his products variation
                    
                    cart_item = CartItem.objects.filter(user=user)

                    ex_var_list = []
                    id = []

                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                            
                    # product_variation = [1,2,3,4,6]
                    # ex_var_list = [4,6,3,5]
                    
                    #  we need to get common product variation
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id = item_id)
                            item.quantity+=1
                            item.user= user
                            item.save()
                        else:
                            cart_item= CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
                            
                    
                    
            except:
                pass
            
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            
            url = request.META.get('HTTP_REFERER')
            # HTTP REFERER will grab the previous url from where you came
            try:
                query = requests.utils.urlparse(url).query
                print('query   :  ', query)
                print('---------------------')
                # next=cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                print('params   :  ', params)
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
            
            
        else:
            messages.warning(request, 'Invalid login credentials')
        
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now Logged out.')
    return redirect('login')

# OTP VERIFICATION:

def otp_mobilenumber(request):
    global mobile_number_for_otp
    
    if request.method == 'POST':
        
        # setting this mobile number as global variable so i can access it in another view (to verify)
        
        mobile_number_for_otp = request.POST.get('phone_number')
        if mobile_number_for_otp is '':
            messages.warning(request, 'You must enter a mobile number')
            return redirect('otp_mobilenumber')
        
        # instead we can also do this by savig this mobile number to session and
        # access it in verify otp:
        # request.session['mobile']= mobile_number
        
        
        user = Account.objects.filter(phone_number=mobile_number_for_otp)
            
        if user:
            verify.send('+91' + str(mobile_number_for_otp))
            return redirect('enter_otp')
        else:
            messages.warning(request,'Mobile number doesnt exist')
    else:
        pass
      
        
    return render(request, 'accounts/otp_mobilenumber.html')

def enter_otp(request):

    if request.method == 'POST':
        
        otp = request.POST.get('otp')
        if verify.check('+91'+ str(mobile_number_for_otp), otp):
            user = Account.objects.get(phone_number=mobile_number_for_otp)
            auth.login(request,user)
            return redirect('home')
        else:
            messages.warning(request,'Invalid OTP')
            return redirect('enter_otp')
        
    
    return render(request,'accounts/enter_otp.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
# 
# 
def forgotPassword(request):
    global mobile_number_forgotPassword
    if request.method == 'POST':
        
        # setting this mobile number as global variable so i can access it in another view (to verify)
        mobile_number_forgotPassword = request.POST.get('phone_number')
        
        # checking the null case
        if mobile_number_forgotPassword is '':
            messages.warning(request, 'You must enter a mobile number')
            return redirect('forgotPassword')
   
        # instead we can also do this by savig this mobile number to session and
        # access it in verify otp:
        # request.session['mobile']= mobile_number
        
        
        user = Account.objects.filter(phone_number=mobile_number_forgotPassword)
            
        if user:  #if user exists
            verify.send('+91' + str(mobile_number_forgotPassword))
            return redirect('forgotPassword_otp')
        else:
            messages.warning(request,'Mobile number doesnt exist')
            return redirect('forgotPassword')
            
    return render(request, 'accounts/forgotPassword.html')

def forgotPassword_otp(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        
        otp = request.POST.get('otp')
        if verify.check('+91'+ str(mobile_number), otp):
            user = Account.objects.get(phone_number=mobile_number)
            if user:
                return redirect('resetPassword')
        else:
            messages.warning(request,'Invalid OTP')
            return redirect('enter_otp')
        
    return render(request,'accounts/forgotPassword_otp.html')

def resetPassword(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')    
        print(str(password1)+' '+str(password2)) #checking
        
        if password1 == password2:
            user = Account.objects.get(phone_number=mobile_number)
            print(user)
            print('old password  : ' +str(user.password))
            
            user.set_password(password1)
            user.save()

            print('new password  : ' +str(user.password))
            messages.success(request, 'Password changed successfully')
            return redirect('login')
        else:
            messages.warning(request, 'Passwords doesnot match, Please try again')
            return redirect('resetPassword')
    
    return render(request, 'accounts/resetPassword.html')