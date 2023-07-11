
from django.urls import path
from . import views


urlpatterns = [
    # login and logout
    path('', views.admin_login, name= 'admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    
    # dashboard
    path('admin_dashboard/', views.admin_dashboard, name= 'admin_dashboard'),
    
    # listing users, products, categories
    path('admin_user/', views.admin_user, name= 'admin_user'),
    path('admin_product/', views.admin_product, name= 'admin_product'),
    path('admin_category/', views.admin_category, name= 'admin_category'),
    
    # user actions
    path('block_user/<int:id>/', views.block_user, name= 'block_user'),
    path('unblock_user/<int:id>/', views.unblock_user, name= 'unblock_user'),
    
    # categories actions
    path('add_category/', views.add_category, name= 'add_category'),
    path('delete_category/<int:id>/', views.delete_category, name= 'delete_category'),
    path('edit_category/<int:id>/', views.edit_category, name= 'edit_category'),
    
    # products actions
    path('add_product/', views.add_product, name= 'add_product'),
    path('delete_product/<int:id>/', views.delete_product, name= 'delete_product'),
    path('edit_product/<int:id>/', views.edit_product, name= 'edit_product'),
    

    


   
] 