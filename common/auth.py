# -*- coding: utf-8 -*-
"""
Common auth checks
"""
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthorization:
    """
    Checks user is authorized.
    """

    def __init__(self, user: User, minimum_level: str) -> None:
        self.user = user
        self.is_authorized = False
        self.minimum_level = minimum_level

        # And here is where some custom auth checks would happen.
