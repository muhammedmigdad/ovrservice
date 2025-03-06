from django import forms
from providers.models import *
from users.models import User
from spareparts.models import *




class ManagerLoginForm(forms.Form):  # Change from ModelForm to Form
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
    
    
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'store', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter store name'}),
            'store': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file-input'}),
        }
        
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'regular_price', 'sale_price', 'store']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter product name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Enter product description', 'rows': 4}),
            'regular_price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter regular price'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter sale price'}),
            'store': forms.Select(attrs={'class': 'form-select'}),
        }
        
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'description', 'image', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your name'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Write your review...', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file-input'}),
            'rating': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Rate (1-5)', 'min': 0, 'max': 5, 'step': 0.1}),
        }
        
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'city', 'state', 'pincode', 'payment_method'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Pincode'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Service Title'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Service Description', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-file-input'}),
        }
        
        
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
        
        

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'is_customer', 'is_provider', 'is_saparepart', 'is_manager']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'is_customer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_provider': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_saparepart': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_manager': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }