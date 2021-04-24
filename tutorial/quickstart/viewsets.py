from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class TemplateFollowViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                   GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass
