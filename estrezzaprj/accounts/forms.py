from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    }))
    confirm_password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    }))
    
    
    class Meta:
        model = Account
        fields =['first_name','last_name','phone_number','email','password']
    
    def __init__(self,*args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = f'{field.replace("_", " ").capitalize()}'
            self.fields[field].widget.attrs['style'] = 'border: none; border-radius: 30px; font-size: 15px; height: 45px; outline: none; width: 100%; color: black; background: rgba(255, 255, 255, 0.1); cursor: pointer; transition: 0.3s; margin-top: 10px; color:#ffffff;'
            self.fields[field].widget.attrs['onfocus'] = 'this.style.outline = "1px solid #F3F4F7"; this.style.transform = "scale(1.04)";'
            self.fields[field].widget.attrs['onblur'] = 'this.style.outline = ""; this.style.transform = ""; this.style.boxShadow = "";'
            
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")
 