# -*- coding: utf-8 -*-
"""
Url config for todo app
"""
from django.urls import path
from django.views.generic import TemplateView

from todo.views import SearchListsView

app_name = 'todo'
urlpatterns = [
    path('search-lists/', SearchListsView.as_view(), name='search_lists'),
    path('', TemplateView.as_view(template_name='todo/home.html'), name='home'),
]
