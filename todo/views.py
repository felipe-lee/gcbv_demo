# -*- coding: utf-8 -*-
"""
Views for todo app
"""
from copy import deepcopy
from typing import Dict, Any, List, Union

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from todo.forms import SearchListsForm
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
