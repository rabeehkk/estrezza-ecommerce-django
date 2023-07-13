
from django.urls import path
from . import views


urlpatterns = [
   
    path('register/', views.register, name= 'register'),
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name= 'logout'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('forgotPassword_otp/', views.forgotPassword_otp, name='forgotPassword_otp'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    
    
    path('otp_mobilenumber/', views.otp_mobilenumber, name= 'otp_mobilenumber'),
    path('enter_otp/', views.enter_otp, name= 'enter_otp'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),

  
    
] 