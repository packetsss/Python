# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from django.urls import path
from . import views # import from current dir

urlpatterns = [
path("<int:id>", views.index, name="id"), # pass id as a variable
path("", views.home, name="home"),
path("create/", views.create, name="create"),
path("view/", views.view, name="view"),
# path("<str:name>", views.name, name="name"),
# path("<str:name>", views.index, name="index"),
]