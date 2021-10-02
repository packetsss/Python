from django.urls import path, include
from django.views.generic import TemplateView

app_name = "blog"

urlpatterns = [
    path("", TemplateView.as_view(template_name="blog/index.html")),
]
