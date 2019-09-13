# -*- coding: utf-8 -*-
"""
Url config for todo app
"""
from django.urls import path
from django.views.generic import TemplateView

from todo.views import SearchListsView, ListTodoListsView, CreateTodoListView, DisplayTodoListView

app_name = 'todo'
urlpatterns = [
    path('list-todo-lists/', ListTodoListsView.as_view(), name='list_todo_lists'),
    path('list-todo-lists/<name_search>/', ListTodoListsView.as_view(), name='list_filtered_todo_lists'),
    path('create-todo-list/', CreateTodoListView.as_view(), name='create_todo_list'),
    path('display-todo-list/<int:pk>/', DisplayTodoListView.as_view(), name='display_todo_list'),
    path('search-lists/', SearchListsView.as_view(), name='search_lists'),
    path('', TemplateView.as_view(template_name='todo/home.html'), name='home'),
]
