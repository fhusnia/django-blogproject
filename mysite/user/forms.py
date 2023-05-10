from django import forms 
from django.contrib.auth.models import User
import re

username_compile = re.compile(r'^\w{5,}$')

class RegisterForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_again = forms.CharField(widget=forms.PasswordInput())


    def save(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        return user
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
         
        if not username_compile.match(username):
            raise forms.ValidationError('Username yazilisi duzgun deil')
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError('bu istifadeci artig ishlenilib')      
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

    
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('bu email artig ishlenilib')      
        return email

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        passworrd_again = self.cleaned_data.get('password_again')

        if password and passworrd_again and password != passworrd_again:
            raise forms.ValidationError('sifre eyni deil')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())

 
        