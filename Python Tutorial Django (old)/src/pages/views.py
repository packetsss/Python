from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    # return HttpResponse("<h1>Hello World</h1>")  # HTML
    return render(request, "home.html", {})  # use a local templete

def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})

def about_view(request, *args, **kwargs):
    my_context = {
        "title": "This is about me??",
        "my_num": 123425,
        "my_list": ["1", "okie", "for ask", "erdf", 1],
        "my_html": "<h1>Hello World</h1>"
    }
    return render(request, "about.html", my_context)

def social_view(request, *args, **kwargs):
    return render(request, "social.html", {})
