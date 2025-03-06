from django import forms
from spareparts.models import *
class MechanicLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "w-full px-4 py-2 rounded-2xl text-black border bg-gray-300"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "w-full px-4 py-2 rounded-2xl text-black border bg-gray-300"}))
    
    
class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['name', 'email', 'phone', 'service', 'details']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Phone'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'details': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Describe your request', 'rows': 4}),
        }
        
