"""
Concrete View Classes

# CreateAPIView (post)
Used for create-only endpoints.

# ListAPIView (list all)
Used for read-only endpoints to represent a collection of model instances.

# RetrieveAPIView (get)
Used for read-only endpoints to represent a single model instance.

# DestroyAPIView (delete)
Used for delete-only endpoints for a single model instance.

# UpdateAPIView (put)
Used for update-only endpoints for a single model instance.

# ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.

# RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.

# RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.

# RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.


To implement a custom permission, override BasePermission and implement either, or both, of the following methods:

.has_permission(self, request, view)
.has_object_permission(self, request, view, obj)
"""

from blog.models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import filters, permissions, viewsets, generics
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAdminUser,
    BasePermission,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissionsOrAnonReadOnly,
)


class PostUserWritePermission(BasePermission):
    message = "Editing posts is restricted to the author only"

    def has_object_permission(self, request, view, obj):
        # if is not author, only allow get, option, head
        if request.method in SAFE_METHODS:
            return True

        # if is author, allow put and delete
        return obj.author == request.user


class PostListDetailFilter(viewsets.ModelViewSet):
    """
    Regex:
    '^' Starts-with search.
    '=' Exact matches.
    '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
    '$' Regex search.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["$slug", "$content"]


class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default create(), retrieve(), update(), partial_update(), destroy() and list() actions.

    Hard for customization
    """

    permission_classes = [IsAuthenticated, ]#PostUserWritePermission]
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs["pk"]  # capture pk item
        print(self.kwargs, queryset)
        return get_object_or_404(Post, slug=item)

    # overwrite default queryset
    def get_queryset(self):
        # print(PostSerializer(list(Post.objects.all())[0]))
        return Post.objects.all()


"""
class PostList(viewsets.ViewSet):
    '''
    Supports (automatically):
    - api/ ^$ [name='post-list']
    - api/ ^\.(?P<format>[a-z0-9]+)/?$ [name='post-list']
    - api/ ^(?P<pk>[^/.]+)/$ [name='post-detail']
    - api/ ^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='post-detail']
    - api/ ^$ [name='api-root']
    - api/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']
    '''
    permission_classes = [IsAuthenticated]
    queryset = Post.post_objects.all()

    def list(self, request):
        serializer_class = PostSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer_class = PostSerializer(post)
        return Response(serializer_class.data)


class PostList(generics.ListCreateAPIView):
    # permissions using groups (Anon is anonymous)
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.post_objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [PostUserWritePermission]
    queryset = Post.objects.all()

    # same serializer_class since same data
    serializer_class = PostSerializer
"""
