# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from django.shortcuts import render, redirect

# Create your views here.
from .forms import RegistrationForm

def register(response):
    if response.method == "POST":
        form = RegistrationForm(response.POST)
        if form.is_valid():
            form.save()
        print(form)
        return redirect("/")
    else:
        form = RegistrationForm()

    return render(response, "register/register.html", {"form": form})