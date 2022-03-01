from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def login(request):
    return render(request, "Login/login.html")

def password_reset(request):
    return render(request, "Login/password_reset_form_12.html")

def logout(request):
    return render(request, "Login/logged_out_20.html")

def password_change(request):
    return render(request, "Login/password_change_form.html")