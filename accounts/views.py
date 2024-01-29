from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # print(first_name, last_name, username, email, password)
        user_obj = User.objects.filter(email=email)

        if user_obj.exists():
            messages.warning(request,"Your Email already exist")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=username)
        user_obj.set_password(password)
        user_obj.save()

        return redirect('/')
            
    return render(request, 'auth/register.html')

def login(request):
    pass