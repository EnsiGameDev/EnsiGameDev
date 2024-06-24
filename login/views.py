from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from login.models import Profil
from django.contrib.auth.forms import AuthenticationForm

def log_in(request):
    user_type = None
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                profil = Profil.objects.get(user=user) #TODO creer si n'existe pas
                user_type = profil.type
                return redirect('/principal/')
    else:
        form = AuthenticationForm()
        if request.user.is_authenticated:
            try:
                profil = Profil.objects.get(user=request.user)
                user_type = profil.type
            except Profil.DoesNotExist:
                user_type = None
                
    context = {
        'form': form,
        'user_type': user_type
    }
    print(user_type)
    return render(request, 'login/connection.html', context)
