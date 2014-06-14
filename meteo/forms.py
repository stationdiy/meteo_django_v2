from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from models import Station

class UserForm(ModelForm):
    email = forms.EmailField(label='Email address', max_length=75)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }
       
        
        
class UserLogForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }
class StationForm(forms.ModelForm):
    class Meta:
        model = Station

