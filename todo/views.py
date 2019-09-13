# -*- coding: utf-8 -*-
"""
Views for todo app
"""
from copy import deepcopy
from typing import Dict, Any, List, Union

from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, ListView, CreateView, DetailView, UpdateView, DeleteView

from todo.forms import SearchListsForm, TodoListForm
from todo.models import TodoListModel


class SearchListsView(FormView):
    """
    View to search through existing lists
    """
    form_class = SearchListsForm
    template_name = 'todo/search_lists.html'
    http_method_names = ['get', 'options']

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Set up form and if data was passed in, validate it, otherwise render page with form.
        :param request: wsgi request
        :return: response for user
        """
        form = self.get_form()

        if request.GET:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self) -> Dict[str, Any]:
        """
        Get kwargs to instantiate form
        :return: form kwargs
        """
        kwargs = super().get_form_kwargs()

        if self.request.GET:
            kwargs['data'] = deepcopy(self.request.GET)

        return kwargs

    def form_valid(self, form) -> HttpResponse:
        """
        Redirect to view that lists todo lists, filtered by name search.
        :param form: validated form
        :return: redirect to another view
        """
        name = form.cleaned_data.get('name')

        return redirect(reverse_lazy('todo:list_filtered_todo_lists', kwargs={'name_search': name}))


def search_lists_view(request):
    if not request.method == 'GET':
        return HttpResponseNotAllowed(['GET'])

    form_kwargs = {}
    if request.GET:
        form_kwargs['data'] = deepcopy(request.GET)

    form = SearchListsForm(**form_kwargs)

    if request.GET and form.is_valid():
        name = form.cleaned_data.get('name')

        return redirect(reverse_lazy('todo:list_filtered_todo_lists', kwargs={'name_search': name}))

    context = {
        'form': form
    }

    return render(request, 'todo/search_lists.html', context)


class ListTodoListsView(ListView):
    """
    View to list TodoLists
    """
    model = TodoListModel
    template_name = 'todo/list_todo_lists.html'

    def get_queryset(self) -> Union[QuerySet, List[TodoListModel]]:
        """
        Returns queryset with everything, or filtered
        :return:
        """
        if 'name_search' in self.kwargs:
            self.queryset = self.model.objects.filter(name__icontains=self.kwargs['name_search'])

        return super().get_queryset()


def list_todo_lists_view(request, name_search=''):
    queryset = TodoListModel.objects.all()
    if name_search:
        queryset = queryset.filter(name__icontains=name_search)

    context = {
        'object_list': queryset,
        'name_search': name_search,
    }
    return render(request, 'todo/list_todo_lists.html', context)


class CreateTodoListView(CreateView):
    """
    View to create new todo lists
    """
    template_name = 'todo/create_todo_list.html'
    form_class = TodoListForm


def create_todo_list_view(request):
    if request.method == 'GET':
        form = TodoListForm()

        return render(request, 'todo/create_todo_list.html', {'form': form})
    elif request.method == 'POST':
        form = TodoListForm(data=deepcopy(request.POST))

        if form.is_valid():
            todo_list = form.save()

            return redirect(todo_list.get_absolute_url())
        else:
            return render(request, 'todo/create_todo_list.html', {'form': form})


class DisplayTodoListView(DetailView):
    """
    View to show detailed view of todo list
    """
    template_name = 'todo/display_todo_list.html'
    model = TodoListModel
    context_object_name = 'todo_list'


class UpdateTodoListView(UpdateView):
    """
    View to update a todo list
    """
    template_name = 'todo/update_todo_list.html'
    form_class = TodoListForm
    model = TodoListModel
    context_object_name = 'todo_list'


class DeleteTodoListView(DeleteView):
    """
    View to delete a todo list
    """
    template_name = 'todo/delete_todo_list.html'
    model = TodoListModel
    context_object_name = 'todo_list'
    success_url = reverse_lazy('todo:list_todo_lists')

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. Overriding to add a message.
        :param request: wsgi request
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        success_message = _(f'Successfully deleted todo list: {self.object}')

        self.object.delete()

        messages.success(request=request, message=success_message)

        return redirect(success_url)
