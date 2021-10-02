from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


urlpatterns = [
    # allow logins using react
    path("auth/", include("drf_social_oauth2.urls", namespace="drf")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    
    # manage users, tokens, refresh tokens
    path("api/user/", include("users.urls", namespace="users")),
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # admin page and api page
    path("admin/", admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
    path("api/", include("blog_api.urls", namespace="blog_api")),
    
    # documentation
    path('docs/', include_docs_urls(title='BlogAPI')),
    path('schema/', get_schema_view(
        title="BlogAPI",
        description="API for the BlogAPI",
        version="1.0.0"
    ), name='openapi-schema'),
]

# local media folder
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)