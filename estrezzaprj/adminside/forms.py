from django import forms
# importing category model from category app
from  category.models import Category
from store.models import Product
#  for auto populating slug field
from django.utils.text import slugify

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        exclude = ['slug']
        fields = ['category_name','description','cat_image']
   
    def __init__(self,*args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = f'{field.replace("_", " ").capitalize()}'
            self.fields[field].widget.attrs['style'] = 'border: none; border-radius: 30px; font-size: 15px; height: 45px; outline: none; color: black; background: rgba(255, 255, 255, 0.1); cursor: pointer; transition: 0.3s; margin-top: 10px; color:#ffffff; text-align: center;'
            self.fields[field].widget.attrs['onfocus'] = 'this.style.outline = "1px solid #F3F4F7"; this.style.transform = "scale(1.04)";'
            self.fields[field].widget.attrs['onblur'] = 'this.style.outline = ""; this.style.transform = ""; this.style.boxShadow = "";'

            
class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['product_name','description','price','images','stock']
        
        
    def __init__(self,*args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = f'{field.replace("_", " ").capitalize()}'
            self.fields[field].widget.attrs['style'] = 'border: none; border-radius: 30px; font-size: 15px; height: 45px; outline: none; color: black; background: rgba(255, 255, 255, 0.1); cursor: pointer; transition: 0.3s; margin-top: 10px; color:#ffffff; text-align: center;'
            
 
    