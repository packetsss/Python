import graphene
from graphene_django import DjangoObjectType

from .models import Books

# just like serializers
class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("id", "title", "excerpt")


class BookQuery(graphene.ObjectType):
    # convert data to graph
    all_books = graphene.List(BooksType)

    def resolve_all_books(root, info):
        return Books.objects.all()


book_schema = graphene.Schema(query=BookQuery)
