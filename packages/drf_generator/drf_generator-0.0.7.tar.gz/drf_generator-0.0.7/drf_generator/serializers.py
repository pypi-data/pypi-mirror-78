#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .settings import SERIALIZER


def serializer_factory(model, mixins=()):
    meta = type('Meta', (), {'fields': "__all__", 'model': model})
    return type('{}Serializer'.format(model.__name__),
                tuple(mixins) + (SERIALIZER,),
                {'Meta': meta})
