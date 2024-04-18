from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
import json

from django.shortcuts import render

def task_form(request):
    if request.method == 'POST':
        # Handle form submission
        title = request.POST.get('title')
        description = request.POST.get('description')
        # Create Task instance or perform other actions as needed
        # Example: Task.objects.create(title=title, description=description)
        return JsonResponse({'message': 'Task added successfully'}, status=201)
    
    # Render the form template for GET requests
    return render(request, 'tasks/task_form.html')
