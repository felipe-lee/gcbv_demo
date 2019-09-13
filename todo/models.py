# -*- coding: utf-8 -*-
"""
models for todo app
"""
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class TodoListModel(models.Model):
    """
    Model to keep todo lists
    """
    name = models.CharField(verbose_name=_('list name'), max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self) -> str:
        """
        Retrieve url to view list
        :return: list url
        """
        return reverse_lazy('todo:display_todo_list', kwargs={'pk': self.id})

    def __str__(self) -> str:
        return self.name


class TodoItemModel(models.Model):
    """
    Model for todo items
    """
    todo_list = models.ForeignKey(TodoListModel, default=None, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        ordering = ('id',)
        unique_together = ('todo_list', 'text')

    def save(self, **kwargs) -> 'TodoItemModel':
        """
        Ensure we save TodoListModel for last_edited field
        :param kwargs: kwargs to pass on to regular save
        :return: saved instance
        """
        instance = super().save(**kwargs)

        self.todo_list.save()

        return instance

    def __str__(self) -> str:
        return self.text
