# -*- coding: utf-8 -*-
"""
Serializers for todo models
"""
from rest_framework import serializers

from todo.models import TodoItemModel


class TodoItemSerializer(serializers.ModelSerializer):
    """
    Serializer for TodoItemModel
    """

    class Meta:
        """
        Define model and fields
        """
        model = TodoItemModel
        fields = ['todo_list', 'text', 'completed']
