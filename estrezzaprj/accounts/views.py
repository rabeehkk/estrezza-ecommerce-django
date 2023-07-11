from django.shortcuts import render,redirect
from . forms import *
from .models import *
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from . import verify

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
            auth.login(request, user)
            return redirect('home')
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
    
    if request.method == 'POST':
        
        # setting this mobile number as global variable so i can access it in another view (to verify)
        global mobile_number_for_otp
        mobile_number_for_otp = request.POST.get('phone_number')
        
        # instead we can also do this by savig this mobile number to session and
        # access it in verify otp:
        # request.session['mobile']= mobile_number
        
        
        user = Account.objects.filter(phone_number=mobile_number_for_otp)
            
        if user:
            verify.send('+91' + str(mobile_number_for_otp))
            return redirect('enter_otp')
        else:
            messages.warning(request,'Mobile number doesnt exist')
      
        
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