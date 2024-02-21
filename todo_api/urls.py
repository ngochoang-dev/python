from .views import TodoListApiView, TodoListDetailView
from django.urls import path

urlpatterns = [
    path('', TodoListApiView.as_view()),
    path('todo/<int:id>', TodoListDetailView.as_view())
]