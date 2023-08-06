# DRF-generator

This library does only **3** things

1. Make serializers from models
```python
import drf_generator

from app import models

UserSerializer = drf_generator.serializer_factory(models.User)
PostSerializer = drf_generator.serializer_factory(models.Post)
# …
```
2. Make model viewsets from models
```python
import drf_generator

from app import models

UserViewSet = drf_generator.view_set_factory(models.User)
PostViewSet = drf_generator.view_set_factory(models.Post)
# …
```
3. Let you register models instead of views in url routers
```python
import drf_generator

from app import models

router = drf_generator.routers.DRYRouter()
router.register(r'users', models.User)
router.register(r'posts', models.Post)
# …
