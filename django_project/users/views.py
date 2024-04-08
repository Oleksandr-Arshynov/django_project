from django.contrib.auth import login as auth_login, logout as django_logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView

def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='quotes:root')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='users:login')
        else:
            return render(request, 'users/register.html', context={"form": form})

    return render(request, 'users/register.html', context={"form": RegisterForm()})
def loginuser(request):
    if request.user.is_authenticated:
       return redirect(to='quotes:root')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='quotes:root')

    return render(request, 'users/login.html', context={"form": LoginForm()})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'

    
@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='quotes:root')

