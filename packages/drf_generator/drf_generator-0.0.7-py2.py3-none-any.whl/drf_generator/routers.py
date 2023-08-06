#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from rest_framework import routers

from .views import view_set_factory


class DRYRouter(routers.DefaultRouter):
    def register(self, prefix, viewset_or_model, base_name=None):
        if issubclass(viewset_or_model, models.Model):
            viewset = view_set_factory(viewset_or_model)
        else:
            viewset = viewset_or_model
        return super(DRYRouter, self).register(prefix,
                                               viewset,
                                               base_name)
