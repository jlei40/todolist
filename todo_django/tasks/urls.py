from django.urls import path
from . import views

urlpatterns = [
    path('tasks/create/', views.task_form, name='task_create'),
    # Other URLs
]
