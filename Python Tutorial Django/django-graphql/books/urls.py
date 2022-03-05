from django.urls import path
from graphene_django.views import GraphQLView

from books.schema import book_schema

urlpatterns = [
    # only need a single URL to access GraphQL
    path("graphql", GraphQLView.as_view(graphiql=True, schema=book_schema)),
]
