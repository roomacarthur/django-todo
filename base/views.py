from base.models import Task
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    """ ensuring that the data provided is specific to the 
        logged in user by asserting tasks = to the users tasks. 
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        # get a count of incomplete items.
        context['count'] = context['tasks'].filter(complete=False).count()
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # fields = ['title', 'description']
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    # auto set user to self on add task form.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskEdit(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
