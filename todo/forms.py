# -*- coding: utf-8 -*-
"""
Forms for todo app
"""
from django import forms
from django.utils.translation import ugettext_lazy as _


class SearchListsForm(forms.Form):
    """
    Form to search for existing lists.
    """
    name = forms.CharField(label=_('list name'), required=True)
