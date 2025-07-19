from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User


def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
        return render(request, 'signin.html',locals())
    else:
        return redirect("/")
    
def logout_view(request):
    logout(request)
    return redirect('signin')