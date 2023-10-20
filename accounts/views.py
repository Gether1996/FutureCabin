from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def logout_view(request):
    logout(request)
    return redirect('homepage')


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
        else:
            messages.error(request, 'Something went wrong.')
            return render(request, 'registration.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})


@login_required
def account(request):
    user = request.user
    return render(request, 'account.html', {'user': user})
