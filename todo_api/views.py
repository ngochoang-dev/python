from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer
from functools import wraps


def check_todo_exist(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        id = kwargs.get('id')
        todo_instance = self.get_object(id)

        if not todo_instance:
            return Response({
                "message": "Not exist this todo."
            }, status=status.HTTP_404_NOT_FOUND)
        return func(*args, todo_instance = todo_instance,  **kwargs)


    return wrapper


# Create your views here.
class TodoListApiView(APIView):
    def get(self, request, *args, **kwargs):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "xxxx"},  status=status.HTTP_400_BAD_REQUEST)

class TodoListDetailView(APIView):
    def get_object(self, id):
        try:
            return Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return None
    
    @check_todo_exist
    def get(self, request, todo_instance, id):
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @check_todo_exist
    def put(self, request,todo_instance, id):
        print(request.data)
        serializer = TodoSerializer(instance = todo_instance, data = request.data, partial = True)
        if serializer.is_valid():
            return Response({"message": "Update completed", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Update failed"}, status=status.HTTP_400_BAD_REQUEST)