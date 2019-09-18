# -*- coding: utf-8 -*-
"""
common urls
"""
from django.conf import settings
from django.urls import path

from common.views import HomeView, home_view

app_name = 'common'

if settings.VIEW_TYPES == 'CBV':
    urlpatterns = [
        path('', HomeView.as_view(), name='home'),
    ]
else:
    urlpatterns = [
        path('', home_view, name='home'),
    ]
