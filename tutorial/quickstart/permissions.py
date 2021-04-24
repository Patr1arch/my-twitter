from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly

from tutorial.quickstart.models import Tweet


class IsTweetAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    The request is tweet from a user, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj: Tweet):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user and
            request.user.is_authenticated and
            obj.author == request.user
        )
