from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet

from django.http import HttpResponse
from django.http import Http404, HttpResponseBadRequest

from tutorial.quickstart.models import Dag, Tweet, FollowerFollows
from rest_framework import viewsets, permissions, mixins

from tutorial.quickstart.permissions import IsTweetAuthorOrReadOnly
from tutorial.quickstart.serializers import UserSerializer, DagSerializer, TweetSerializer, FollowerFollowsSerializer, \
    FollowsSerializer, FollowedSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'


class DagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Dag.objects.all()
    serializer_class = DagSerializer


class TweetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsTweetAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserTweetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    def get_queryset(self):
        return self.queryset.filter(author__username=self.kwargs['parent_lookup_username'])


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return self.queryset.filter(author=User.objects.get(
        #     followers=FollowerFollows.objects.get(follower=self.request.user)))
        return self.queryset.filter(author__followers__follower=self.request.user)


class FollowViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = FollowerFollows.objects
    serializer_class = FollowerFollowsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not User.objects.filter(username=self.kwargs[self.lookup_field]):
            raise Http404
        if self.queryset.filter(follower=self.request.user,
                                follows=User.objects.get(
                                    username=self.kwargs[self.lookup_field])):
            raise Http404  # TODO: make with Http400, all checks in serializer!
        serializer.save(follower=self.request.user,
                        follows=User.objects.get(
                            username=self.kwargs[self.lookup_field]))

    # Проверка на существование и фолловинг на самого себя и не дублировать записи

    def get_object(self):
        return self.queryset.filter(follower=self.request.user,
                                    follows__username=self.kwargs[self.lookup_field])


class FollowsListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FollowerFollows.objects
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FollowsSerializer

    def get_queryset(self):
        return self.queryset.filter(follower__username=self.kwargs['parent_lookup_username'])


class FollowedListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FollowerFollows.objects
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FollowedSerializer

    def get_queryset(self):
        return self.queryset.filter(follows__username=self.kwargs['parent_lookup_username'])
