from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate,get_user_model
from .forms import UserLoginForm,UserRegistrationForm
# Create your views here.


def login_view(request):
    title="Login"
    next=request.GET.get('next')
    form=UserLoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user=authenticate(username=username,password=password)
        login(request,user)
        if next:
            return redirect(next)
        return redirect('/')

    context={'form':form,
            'title':title,            }
    return render(request,"login.html",context)

def register_view(request):
    title="Register"
    next=request.GET.get('next')
    form=UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        email=form.cleaned_data.get('email')
        password=form.cleaned_data.get('password')
        user.set_password(password)
        user.email=email
        user.save()
        user=authenticate(username=user.username,password=password)
        login(request,user)
        if next:
            return redirect(next)
        return redirect('/')

    context={'form':form,
            'title':title,            }
    return render(request,"login.html",context)

def logout_view(request):
    logout(request)
    return redirect('/')
    return render(request,"login.html")