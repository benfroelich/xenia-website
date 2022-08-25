from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages


def register_request(request):
    template_name = 'registration/register.html'
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('/')
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = NewUserForm()
        return render(request=request, template_name=template_name, context={'registration_form':form})

