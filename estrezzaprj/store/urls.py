from django.urls import path
from . import views



urlpatterns = [
    path('', views.store, name='store'),
    
    # for category wise urls like '...../shirts'
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    
    # for individual product page
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'), 
    
    # for search bar
    path('search/', views.search, name= "search"),
]