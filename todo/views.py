from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Todo
from . import models
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

from django.shortcuts import get_object_or_404


def signup(request):
    # clear message list ...
    list(messages.get_messages(request))

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(username,email,password)

        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')

        newUser = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully!')
        newUser.save()

        return redirect('login')

    return render(request,'signup.html')

def login_view(request):
    # clear message list ...
    list(messages.get_messages(request))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        data = {
            'user':username,
        }

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have logged in successfully.')
            return redirect('home')  
        else:
            # Invalid credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  

    return render(request, 'login.html')

def home(request):
    if request.method == 'POST':
        newTask = request.POST.get("task")
        print(request.user,newTask)   
        obj = models.Todo(title=newTask,user=request.user)
        obj.save()
        return redirect('home')
    result = models.Todo.objects.filter(user = request.user).order_by('date')
    return render(request,'todo.html',{'tasks':result})

def delete_task(request,id):
    if request.method == 'POST' and request.user.is_authenticated:
        task = get_object_or_404(Todo, srno=id, user=request.user)
        task.delete()
    return redirect('home')

def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)        
        # clear message list ...
        list(messages.get_messages(request))
        messages.success(request, 'You have logged out successfully.')
        return redirect('login')