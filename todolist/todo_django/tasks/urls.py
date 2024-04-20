from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    # Tags URLs
    path("tags/", views.TagListView.as_view(), name="tag_list"),
    path("tags/<int:pk>/", views.TagDetailView.as_view(), name="tag_detail"),
    path("tags/new/", views.TagCreateView.as_view(), name="tag_create"),
    path("tags/update/<int:pk>/", views.TagUpdateView.as_view(), name="tag_update"),
    path('tag/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),
    
    # Tasks URLs
    path("tasks/", views.TaskListView.as_view(), name="task_list"),
    path("tasks/new/", views.TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("tasks/update/<int:pk>/", views.TaskUpdateView.as_view(), name="task_update"),
    path("tasks/delete/<int:pk>/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/update_bis/<int:pk>/", views.TaskUpdatebisView.as_view(), name="task_update_bis"),
    path("tasks/js/<int:pk>/", views.TaskDetailJsView.as_view(), name="task_detail_js"),
]
