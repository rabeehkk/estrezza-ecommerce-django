
from django.urls import path
from . import views


urlpatterns = [
   
    path('register/', views.register, name= 'register'),
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name= 'logout'),
    path('otp_mobilenumber/', views.otp_mobilenumber, name= 'otp_mobilenumber'),
    path('enter_otp/', views.enter_otp, name= 'enter_otp'),
  
    
] 