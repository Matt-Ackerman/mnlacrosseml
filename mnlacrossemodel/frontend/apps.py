# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = 'mnlacrossemodel.frontend'

    def ready(self):
        """
        This is triggered on app startup. It is necessary to start our runner, which will predict games, store data, etc.
        """
        print('--- starting app')
        from mnlacrossemodel.backend import orchestrator
        orchestrator.start()
