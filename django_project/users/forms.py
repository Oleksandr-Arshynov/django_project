from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, TextInput, FileInput, EmailInput, EmailField, PasswordInput
    
class RegisterForm(UserCreationForm):
    username = CharField(max_length=16, min_length=3, required=True,
                widget=TextInput(attrs={'class': 'form-label'}))
    email = EmailField(max_length=16, min_length=3, required=True,
                widget=EmailInput(attrs={'class': 'form-label'}))
    password1 = CharField(max_length=25, required=True,
                widget=PasswordInput(attrs={'class': 'form-label'}))
    password2 = CharField(max_length=25, required=True,
                widget=PasswordInput(attrs={'class': 'form-label'}))
    
        
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = CharField(max_length=16, min_length=3, required=True,
                widget=TextInput(attrs={'class': 'form-label'}))
    password = CharField(max_length=25, required=True,
                widget=PasswordInput(attrs={'class': 'form-label'}))
    
    
    class Meta:
        model = User
        fields = ('username', 'password')
