from django.contrib import admin
from .models import Todo
# Register your models here.
class TodoListAdmin(admin.ModelAdmin):
    list_display = ("task", "completed", "timestamp", "updated", "user")

admin.site.register(Todo, TodoListAdmin)