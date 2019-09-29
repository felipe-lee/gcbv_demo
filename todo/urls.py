# -*- coding: utf-8 -*-
"""
Url config for todo app
"""
from django.conf import settings
from django.urls import path
from django.views.generic import RedirectView, TemplateView

from todo.views import CreateTodoListView, DeleteTodoListView, DisplayTodoListView, ListAndFilterTodoListsView, \
    ListTodoListsView, SearchListsView, UpdateTodoListView, create_todo_list_view, delete_todo_list_view, \
    display_todo_list_view, home_view, list_todo_lists_view, redirect_to_list_todo_lists_view, search_lists_view, \
    update_todo_list_view

app_name = 'todo'

if settings.VIEW_TYPES == 'CBV':
    print('using class-based views')

    urlpatterns = [
        path('show-all-lists/', RedirectView.as_view(pattern_name='todo:list_and_filter_todo_lists'),
             name='show_all_lists'),
        path('list-todo-lists/', ListTodoListsView.as_view(), name='list_todo_lists'),
        path('list-todo-lists/<name_search>/', ListTodoListsView.as_view(), name='list_filtered_todo_lists'),
        path('lists/', ListAndFilterTodoListsView.as_view(), name='list_and_filter_todo_lists'),
        path('create-todo-list/', CreateTodoListView.as_view(), name='create_todo_list'),
        path('display-todo-list/<int:pk>/', DisplayTodoListView.as_view(), name='display_todo_list'),
        path('update-todo-list/<int:pk>/', UpdateTodoListView.as_view(), name='update_todo_list'),
        path('delete-todo-list/<int:pk>/', DeleteTodoListView.as_view(), name='delete_todo_list'),
        path('search-lists/', SearchListsView.as_view(), name='search_lists'),
        path('', TemplateView.as_view(template_name='todo/home.html'), name='home'),
    ]
else:
    print('using function-based views')

    urlpatterns = [
        path('show-all-lists/', redirect_to_list_todo_lists_view, name='show_all_lists'),
        path('list-todo-lists/', list_todo_lists_view, name='list_todo_lists'),
        path('list-todo-lists/<name_search>/', list_todo_lists_view, name='list_filtered_todo_lists'),
        path('create-todo-list/', create_todo_list_view, name='create_todo_list'),
        path('display-todo-list/<int:pk>/', display_todo_list_view, name='display_todo_list'),
        path('update-todo-list/<int:pk>/', update_todo_list_view, name='update_todo_list'),
        path('delete-todo-list/<int:pk>/', delete_todo_list_view, name='delete_todo_list'),
        path('search-lists/', search_lists_view, name='search_lists'),
        path('', home_view, name='home'),
    ]
