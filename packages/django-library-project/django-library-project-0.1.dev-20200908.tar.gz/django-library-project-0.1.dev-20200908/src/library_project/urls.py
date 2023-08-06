# Copyright (C) 2020
# Author: Stuart MacKay
# Contact: smackay@flagstonesoftware.com

from django.urls import path

from .views import IndexView

urlpatterns = [path("", IndexView.as_view(), name="app_index")]
