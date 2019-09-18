# -*- coding: utf-8 -*-
"""
Tests for common views
"""
from django.test import TestCase
from django.urls import reverse_lazy


class HomePageTest(TestCase):

    def test_uses_home_template(self) -> None:
        response = self.client.get(reverse_lazy('common:home'))

        self.assertTemplateUsed(response, 'common/home.html')
