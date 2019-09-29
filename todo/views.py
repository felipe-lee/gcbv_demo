# -*- coding: utf-8 -*-
"""
Views for todo app
"""
from copy import deepcopy
from typing import List, Union

from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from rest_framework import viewsets

from common.views import FormListView, GetFormView
from todo.forms import SearchListsForm, TodoListForm
from todo.models import TodoItemModel, TodoListModel
from todo.serializers import TodoItemSerializer


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Render todo home page
    :param request: user wsgi request
    :return: home page
    """
    return render(request=request, template_name='todo/home.html')


class SearchListsView(GetFormView):
    """
    View to search through existing lists
    """
    form_class = SearchListsForm
    template_name = 'todo/search_lists.html'
    http_method_names = ['get', 'options']

    def form_valid(self, form) -> HttpResponse:
        """
        Redirect to view that lists todo lists, filtered by name search.
        :param form: validated form
        :return: redirect to another view
        """
        name = form.cleaned_data.get('name')

        return redirect(reverse_lazy('todo:list_filtered_todo_lists', kwargs={'name_search': name}))


def search_lists_view(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    View to search through existing lists
    :param request: wsgi request
    :return: template with form to search through lists, or redirect to view that will filter lists
    """
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
        Filter queryset, if we need to.
        :return: Returns queryset, either full or filtered
        """
        queryset = super().get_queryset()

        if 'name_search' in self.kwargs:
            queryset = queryset.filter(name__icontains=self.kwargs['name_search'])

        return queryset


def list_todo_lists_view(request: HttpRequest, name_search='') -> HttpResponse:
    """
    View to list TodoLists
    :param request: wsgi request
    :param name_search: string to filter queryset by
    :return: template with todo lists
    """
    queryset = TodoListModel.objects.all()
    if name_search:
        queryset = queryset.filter(name__icontains=name_search)

    context = {
        'object_list': queryset,
        'name_search': name_search,
    }
    return render(request, 'todo/list_todo_lists.html', context)


def redirect_to_list_todo_lists_view(request: HttpRequest) -> HttpResponseRedirect:
    """
    Redirects to the new url we want users to use.
    :param request: wsgi request
    :return: redirect to new url
    """
    return redirect(to='todo:list_todo_lists')


class ListAndFilterTodoListsView(FormListView):
    """
    List and possibly filter todo lists
    """
    form_class = SearchListsForm
    model = TodoListModel
    template_name = 'todo/list_and_filter_todo_lists.html'

    def filter_queryset(self) -> QuerySet:
        """
        Filter queryset based on input name
        :return: filtered queryset
        """
        queryset = super().filter_queryset()

        list_name = self.form.cleaned_data.get('name')

        return queryset.filter(name__icontains=list_name)


class CreateTodoListView(CreateView):
    """
    View to create new todo lists
    """
    template_name = 'todo/create_todo_list.html'
    form_class = TodoListForm


def create_todo_list_view(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    View to create new todo lists
    :param request: wsgi request
    :return: template with form to create new list, or redirect to detail page of list
    """
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


def display_todo_list_view(request: HttpRequest, pk: int) -> HttpResponse:
    """
    view to show detailed view of todo list
    :param request: wsgi request
    :param pk: pk of todo list
    :return: template with list details
    """
    todo_list = TodoListModel.objects.get(id=pk)

    return render(request, 'todo/display_todo_list.html', {'todo_list': todo_list})


class UpdateTodoListView(UpdateView):
    """
    View to update a todo list
    """
    template_name = 'todo/update_todo_list.html'
    form_class = TodoListForm
    model = TodoListModel
    context_object_name = 'todo_list'


def update_todo_list_view(request: HttpRequest, pk: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    View to update a todo list
    :param request: wsgi request
    :param pk: pk of todo list
    :return: template with form to edit todo list, or redirect to details page
    """
    todo_list = TodoListModel.objects.get(id=pk)

    context = {
        'todo_list': todo_list
    }

    if request.method == 'GET':
        context['form'] = TodoListForm(instance=todo_list)

        return render(request, 'todo/update_todo_list.html', context)
    elif request.method == 'POST':
        form = TodoListForm(data=deepcopy(request.POST), instance=todo_list)

        if form.is_valid():
            todo_list = form.save()

            return redirect(todo_list.get_absolute_url())
        else:
            context['form'] = form
            return render(request, 'todo/update_todo_list.html', {'form': form})


class DeleteTodoListView(DeleteView):
    """
    View to delete a todo list
    """
    template_name = 'todo/delete_todo_list.html'
    model = TodoListModel
    context_object_name = 'todo_list'
    success_url = reverse_lazy('todo:list_and_filter_todo_lists')

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


def delete_todo_list_view(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """
    delete a todo list
    :param request: wsgi request
    :param pk: pk of todo list
    :return: redirect to full listing page
    """
    todo_list = TodoListModel.objects.get(id=pk)

    if request.method == 'GET':
        return render(request, 'todo/delete_todo_list.html', {'todo_list': todo_list})
    elif request.method == 'POST':
        success_message = _(f'Successfully deleted todo list: {todo_list}')

        todo_list.delete()

        messages.success(request=request, message=success_message)

        return redirect(reverse_lazy('todo:list_and_filter_todo_lists'))


class TodoItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows todo items to be viewed or edited
    """
    queryset = TodoItemModel.objects.all()
    serializer_class = TodoItemSerializer
