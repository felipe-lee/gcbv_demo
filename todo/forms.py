# -*- coding: utf-8 -*-
"""
Forms for todo app
"""
from django import forms
from django.utils.translation import ugettext_lazy as _

from todo.models import TodoListModel


class SearchListsForm(forms.Form):
    """
    Form to search for existing lists.
    """
    name = forms.CharField(label=_('list name'), required=True)


class TodoListForm(forms.ModelForm):
    """
    Form to create and edit todo lists
    """

    class Meta:
        """
        Define modelform options
        """
        model = TodoListModel
        fields = ['name']
