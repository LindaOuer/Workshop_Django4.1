from django.shortcuts import render, redirect
from django.contrib.auth import login

# Create your views here.


def register(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        user = UserRegistrationForm(request.POST)
        login(request, user)
        return redirect('events_listC')
    return render(request, 'registration/login.html', {'form': form})
