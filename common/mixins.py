# -*- coding: utf-8 -*-
"""
Common mixins
"""
from typing import Optional

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _

from common.auth import UserAuthorization


class StaffViewAuthorizationMixin:
    """
    Checks user auth to ensure they are authorized for
    """
    minimum_level = None

    def setup(self, request, *args, **kwargs) -> None:
        """
        Sets some instance attrs.
        :param request: wsgi request
        :param args: view args
        :param kwargs: view kwargs
        """
        self.user_auth: Optional[UserAuthorization] = None

        super().setup(request, *args, **kwargs)

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied(_('You are not authorized to view this site. Please contact system administrators '
                                     'if this is a mistake.'))

        self.user_auth = UserAuthorization(request.user, minimum_level=self.minimum_level)

        if not self.user_auth.is_authorized:
            raise PermissionDenied(_('You are not authorized for the page you attempted to access. Please contact '
                                     'system administrators if this is a mistake.'))

        return super().dispatch(request, *args, **kwargs)
