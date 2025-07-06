from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
import os 

from .models import UserRegister, Create_classroom

class UserRegisterForm(forms.ModelForm):
    # Add a password confirmation field
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm Password'
    )

  

    
    class Meta:
        model = UserRegister
        fields = ['full_name', 'username', 'email', 'phone', 'password', 'gender', 'profile']
        
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your 10-digit phone number'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a strong password'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'profile': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
        labels = {
            'full_name': 'Full Name',
            'username': 'Username',
            'email': 'Email',
            'phone': 'Phone Number',
            'password': 'Password',
            'gender': 'Gender',
            'profile': 'Profile Picture'
        }
        
        help_texts = {
            'username': 'Letters, digits and @/./+/-/_ only.',
            'password': 'Must be at least 8 characters with numbers and special characters.',
            'phone': 'Enter a 10-digit phone number without spaces or dashes.'
        }
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name) < 3:
            raise ValidationError("Full name must be at least 3 characters long.")
        return full_name
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Username validation: alphanumeric + some special chars
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and @/./+/-/_ characters.")
        # Check if username already exists
        if UserRegister.objects.filter(username=username).exists() and not self.instance.pk:
            raise ValidationError("This username is already taken.")
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if email already exists
        if UserRegister.objects.filter(email=email).exists() and not self.instance.pk:
            raise ValidationError("This email is already registered.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Ensure phone is exactly 10 digits
        if not re.match(r'^\d{10}$', phone):
            raise ValidationError("Phone number must be exactly 10 digits.")
        # Check if phone already exists
        if UserRegister.objects.filter(phone=phone).exists() and not self.instance.pk:
            raise ValidationError("This phone number is already registered.")
        return phone
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Password strength validation
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")
        return password
    
def clean_profile(self):
    profile = self.cleaned_data.get('profile')
    if profile:
        # Check file size (limit to 2MB)
        if profile.size > 2 * 1024 * 1024:
            raise ValidationError("Image file size must be less than 2MB.")
        
        # Check file extension
        valid_extensions = ['jpg', 'jpeg', 'png']
        import os
        ext = os.path.splitext(profile.name)[1][1:].lower()
        if ext not in valid_extensions:
            raise ValidationError("Unsupported file extension. Use jpg, jpeg, or png.")
        
        # Replace spaces in filename with underscores
        
    
    return profile
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords don't match.")
        
        return cleaned_data
    

class UserLoginForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        label='Username'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        label='Password'
    )
    
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Remember me'
    )
    
    class Meta:
        model = UserRegister
        fields = ['username', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            try:
                # Only check if user exists, actual authentication happens in the view
                UserRegister.objects.get(username=username)
            except UserRegister.DoesNotExist:
                self.add_error('username', "Username or password is incorrect.")
        
        return cleaned_data

     
class OTPVerificationForm(forms.Form):

    otp = forms.IntegerField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit OTP',
            'class': 'otp-input',
            'maxlength': '6'
        })
    )
    
    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if otp < 100000 or otp > 999999:
            raise forms.ValidationError("OTP must be a 6-digit number")
        return otp
    


from django import forms
from .models import Create_classroom
from django.core.exceptions import ValidationError
import os

class CreateClassroomForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter classroom title'}),
        label='Classroom Title'
    )

    techer_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter teacher name'}),
        label='Teacher Name'
    )

    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Upload File'
    )

    class Meta:
        model = Create_classroom
        fields = ['title', 'techer_name', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 5 * 1024 * 1024:
                raise ValidationError("File size must be less than 5MB.")
            ext = os.path.splitext(file.name)[1][1:].lower()
            if ext not in ['pdf', 'docx', 'pptx']:
                raise ValidationError("Unsupported file extension. Use pdf, docx, or pptx.")
        return file

class ClassroomSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by teacher name or class code'
        })
    )
