# -*- coding: utf-8 -*-
"""
Common Views
"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """
    Render home page
    :param request: user request
    :return: response with home page
    """
    return render(request=request, template_name='common/home.html')
