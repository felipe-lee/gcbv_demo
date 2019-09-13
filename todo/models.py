# -*- coding: utf-8 -*-
"""
models for todo app
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TodoListModel(models.Model):
    """
    Model to keep todo lists
    """
    name = models.CharField(verbose_name=_('list name'), max_length=200)


class TodoItemModel(models.Model):
    """
    Model for todo items
    """
    todo_list = models.ForeignKey(TodoListModel, default=None, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        ordering = ('id',)
        unique_together = ('todo_list', 'text')

    def __str__(self) -> str:
        return self.text
