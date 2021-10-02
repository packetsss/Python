from django.urls import path, include
from .views import CustomUserCreate  # , BlacklistTokenUpdateView

app_name = "users"

urlpatterns = [
    # create new user
    path("register/", CustomUserCreate.as_view(), name="create_user"),
    
    # path("logout/blacklist/", BlacklistTokenUpdateView.as_view(), name="blacklist"),
]
