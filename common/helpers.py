# -*- coding: utf-8 -*-
"""
Common helper functions
"""
from functools import wraps
from typing import Callable, TypeVar

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

RT = TypeVar('RT')
FT = Callable[..., RT]


def my_awesome_decorator(func: FT) -> FT:
    """
    Awesome wrapper
    :param func: function to wrap
    :return: wrapped function
    """

    @wraps(wrapped=func)
    def func_wrapper(*args, **kwargs) -> RT:
        """
        Wrap function
        :return: return of wrapped function
        """
        request = args[0]
        messages.info(request, _('Welcome!'))
        return func(*args, **kwargs)

    return func_wrapper
