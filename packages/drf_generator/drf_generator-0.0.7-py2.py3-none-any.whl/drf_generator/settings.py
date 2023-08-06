from django.conf import settings
import importlib


def proper_import(full_path):
    package, name = full_path.rsplit('.', 1)
    return getattr(importlib.import_module(package), name)


default_settings = {
    'VIEWSET': 'rest_framework.viewsets.ReadOnlyModelViewSet',
    'SERIALIZER': 'rest_framework.serializers.HyperlinkedModelSerializer',
}
default_settings.update(getattr(settings, 'DRF_GENERATOR', {}))

VIEWSET = proper_import(default_settings['VIEWSET'])
SERIALIZER = proper_import(default_settings['SERIALIZER'])
