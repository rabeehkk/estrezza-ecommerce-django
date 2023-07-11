from django.contrib import admin
from .models import Product,Variation

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','is_available','slug')
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')


# product model
admin.site.register(Product, ProductAdmin)
# variation model
admin.site.register(Variation, VariationAdmin)