from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, PostListDetailFilter

app_name = "blog_api"

# use router for viewsets
router = DefaultRouter()
router.register("", PostViewSet, basename="post")
router.register("search/custom", PostListDetailFilter, basename="postsearch")

urlpatterns = router.urls

"""
urlpatterns = [
    path("", PostList.as_view(), name="listcreate"),
    path("<int:pk>/", PostDetail.as_view(), name="detailcreate"),
]
"""
