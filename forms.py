from django import forms
from models import Station
from django.contrib.auth.models import User

actioner_choices = ('Off', 'On')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
   

class StationForm(forms.ModelForm):
    actioner1 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=actioner_choices)
    actioner2 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=actioner_choices)
    actioner3 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=actioner_choices)
    class Meta:
        model = Station
        fields = ('MAC', 'address', 'country', 'city', 'actioner1', 'actioner2', 'actioner3')
