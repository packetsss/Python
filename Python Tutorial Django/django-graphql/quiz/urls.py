from django.urls import path
from graphene_django.views import GraphQLView
from .schema import quiz_schema

urlpatterns = [
    # Only a single URL to access GraphQL
    path("graphql", GraphQLView.as_view(graphiql=True, schema=quiz_schema)),
]