# -*- coding: utf-8 -*-
"""
Url config for todo app
"""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'todo'
urlpatterns = [
    path('', TemplateView.as_view(template_name='todo/home.html')),
]
