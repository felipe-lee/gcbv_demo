# -*- coding: utf-8 -*-
"""
Common Views
"""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Render home page
    """
    template_name = 'common/home.html'
