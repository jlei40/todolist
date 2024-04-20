from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.forms.models import model_to_dict
from django.views import View
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import JsonResponse
import json

from .models import Tag, Task
from .forms import TaskForm

class TagListView(ListView):
    model = Tag
    
class TagDetailView(DetailView):
    model = Tag

class TagCreateView(CreateView):
    model = Tag
    fields = ["name", "homework"]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Tag "{tag_name}" has been created'.format(
                tag_name=self.object.name))
        return response

    def get_success_url(self):
    	return reverse_lazy("tasks:tag_detail", args=[self.object.id])

class TagUpdateView(UpdateView):
    model = Tag
    fields = ["name", "homework"]
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Tag "{tag_name}" has been updated'.format(
                tag_name=self.object.name))
        return response
    
    def get_success_url(self):
        return reverse_lazy("tasks:tag_detail", args=[self.object.id])

class TaskListView(ListView):
    model = Task

class TaskDetailView(DetailView):
    model = Task

class TaskCreateView(CreateView):
    model = Task
    fields = ["name", "description", "homework", "tags",  "date"]

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Task "{task_name}" has been created'.format(
                task_name=self.object.name))
        return response
    
    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", args=[self.object.id])
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       tag_list = list(Tag.objects.all().values())
       context["tag_list"] = tag_list
       context["tag_list"] = json.dumps(tag_list)
       print("context", context)
       return context

class TaskUpdateView(UpdateView):
    model = Task
    template_name_suffix = '_edit'
    fields = ["name", "description", "homework", "tags",  "date"]
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Task "{task_name}" has been updated'.format(
                task_name=self.object.name))
        return response
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       task_dico = model_to_dict(self.object)
       task_dico["date"] = task_dico["date"].strftime(
           "%Y-%m-%d"
       )
       tags = task_dico["tags"]
       task_tag_list = []
       for tag in tags:
           task_tag_list.append({"id": tag.id, "name": tag.name})
       task_dico["tags"] = json.dumps(task_tag_list)
       tag_list = list(Tag.objects.all().values())
       context["task_dict"] = json.dumps(task_dico)
       context["tag_list"] = json.dumps(tag_list)
       print("context", context)
       return context
    
    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", args=[self.object.id])

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task_list")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Task "{task_name}" has been deleted'.format(
                task_name=self.object.name))
        return response

class TaskUpdatebisView(View):
    def post(self, request, *args, **kwargs):
       task = get_object_or_404(Task, pk=self.kwargs["pk"])
       form = TaskForm(request.POST, instance=task)
       if form.is_valid():
           form.save()
           return JsonResponse({"success": True})
       else:
           return JsonResponse({"success": False, "errors": form.errors})
    
class TaskDetailbisView(TemplateView):
    template_name = "tasks/task_detailbis.html"
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_id'] = self.kwargs["pk"]
        return context
    
class TaskDetailJsView(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        task_js = model_to_dict(task)
        task_js["tags"] = []
        for tag in task.tags.values():
            task_js["tags"].append(tag)
        return JsonResponse({"task": task_js})
