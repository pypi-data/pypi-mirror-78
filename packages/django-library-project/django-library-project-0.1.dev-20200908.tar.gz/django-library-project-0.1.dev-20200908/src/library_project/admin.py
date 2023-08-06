# Copyright (C) 2020
# Author: Stuart MacKay
# Contact: smackay@flagstonesoftware.com

from django.contrib import admin

from . import models


@admin.register(models.Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
