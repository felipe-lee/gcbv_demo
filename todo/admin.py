# -*- coding: utf-8 -*-
"""
admin config for todo app
"""
from django.contrib import admin

from todo.models import TodoListModel, TodoItemModel

admin.site.register([TodoListModel, TodoItemModel])
