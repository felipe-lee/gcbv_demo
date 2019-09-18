# -*- coding: utf-8 -*-
"""
gcbv_demo URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from common.views import HomeView, home_view

urlpatterns = [
    path('todo/', include('todo.urls', namespace='todo')),
    path('mage/', admin.site.urls),
]

if settings.VIEW_TYPES == 'CBV':
    urlpatterns.append(path('', HomeView.as_view(), name='home'))
else:
    urlpatterns.append(path('', home_view, name='home'))
