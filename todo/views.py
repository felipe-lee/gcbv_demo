# -*- coding: utf-8 -*-
"""
Views for todo app
"""
from copy import deepcopy
from typing import Dict, Any

from django.http import HttpRequest, HttpResponse
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


class ListTodoListsView(ListView):
    """
    View to list TodoLists
    """
    model = TodoListModel
    template_name = 'todo/list_todo_lists.html'
