# -*- coding: utf-8 -*-
"""
gcbv_demo URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('todo/', include('todo.urls', namespace='todo')),
    path('mage/', admin.site.urls),
    path('', include('common.urls', namespace='common'))
]
