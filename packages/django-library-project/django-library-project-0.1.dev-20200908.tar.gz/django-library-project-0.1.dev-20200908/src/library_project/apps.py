# Copyright (C) 2020
# Author: Stuart MacKay
# Contact: smackay@flagstonesoftware.com

from django.apps import AppConfig


def setup_app_settings():
    from django.conf import settings

    from . import settings as defaults

    for name in dir(defaults):
        if name.isupper() and not hasattr(settings, name):
            setattr(settings, name, getattr(defaults, name))


class LibraryProjectConfig(AppConfig):
    name = "library_project"
    verbose_name = "Library Project"

    def ready(self):
        setup_app_settings()
