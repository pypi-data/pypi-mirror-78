# Copyright (C) 2020
# Author: Stuart MacKay
# Contact: smackay@flagstonesoftware.com

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "library_project/index.html"
