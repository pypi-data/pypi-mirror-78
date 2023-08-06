#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .settings import VIEWSET
from .serializers import serializer_factory
# Default view setting


def view_set_factory(model, serializer=None):
    return type('{}ViewSet'.format(model.__name__),
                (VIEWSET,),
                {
                    'queryset': model.objects.all(),
                    'serializer_class': (serializer or
                                         serializer_factory(model)),
                })
