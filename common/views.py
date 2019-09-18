# -*- coding: utf-8 -*-
"""
Common Views
"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Render home page
    """
    template_name = 'common/home.html'


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Render todo home page
    :param request: user wsgi request
    :return: home page
    """
    return render(request=request, template_name='common/home.html')
