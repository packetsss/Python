# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from django.contrib import admin

# Register your models here.
from.models import ToDoList, Item
admin.site.register(ToDoList)
admin.site.register(Item)
