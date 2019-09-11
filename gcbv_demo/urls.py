# -*- coding: utf-8 -*-
"""
gcbv_demo URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from common.views import HomeView

urlpatterns = [
    path('todo/', include('todo.urls', namespace='todo')),
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home')
]
