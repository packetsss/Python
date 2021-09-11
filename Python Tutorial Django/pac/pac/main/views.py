# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import Create_list

def index(response, id):
    lst = ToDoList.objects.get(id=id)
    dic = {"list": lst}
    
    if lst in response.user.todolist.all():
        if response.method == "POST":
            # Our dic be like: {"save": ["save"], "c1": ["clicked"]}
            print(response.POST)
            if response.POST.get("save"):
                for item in lst.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")
                if len(txt) > 0:
                    lst.item_set.create(text=txt, complete=False)
                else:
                    print("Invalid input")

        
        return render(response, "main/list.html", dic)
    return render(response, "main/view.html", dic)

def home(response):
    return render(response, "main/home.html", {})

def create(response):
    if response.method == "POST":
        form = Create_list(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)
        
        return HttpResponseRedirect(f"/{t.id}")

    else:
        pass    
    form = Create_list()
    dic = {"form": form}
    return render(response, "main/create.html", dic)


def view(response):
    return render(response, "main/view.html", {})

# def id(response, id):
#     lst = ToDoList.objects.get(id=id)
#     return HttpResponse(f"<h1>{lst.name}</h1>")

# def name(response, name):
#     lst = ToDoList.objects.get(name=name)
#     item = lst.item_set.get(id=1)
#     return render(response, "main/base.html", {})