# -*- coding: utf-8 -*-
"""
Url config for todo app
"""
from django.urls import path
from django.views.generic import TemplateView

from todo.views import SearchListsView, ListTodoListsView

app_name = 'todo'
urlpatterns = [
    path('list-todo-lists/', ListTodoListsView.as_view(), name='list_todo_lists'),
    path('search-lists/', SearchListsView.as_view(), name='search_lists'),
    path('', TemplateView.as_view(template_name='todo/home.html'), name='home'),
]
