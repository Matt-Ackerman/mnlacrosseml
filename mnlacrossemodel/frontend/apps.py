# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = 'mnlacrossemodel.frontend'

    def app_startup(self):
        """
        1. This function runs on app startup.
        2. It starts our chron job, which uses PredictionRunner.py
           to update our predictions and prediction results front end tables.
        """
        print('--- starting app')
        from mnlacrossemodel.backend import prediction_runner_chron
        prediction_runner_chron.start()
