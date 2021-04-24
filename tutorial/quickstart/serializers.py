from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from tutorial.quickstart.models import Dag, Tweet, FollowerFollows


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class DagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dag
        fields = ['url', 'name', 'owner']


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'photo', 'created', 'author']


class FollowerFollowsSerializer(serializers.HyperlinkedModelSerializer):
    # follower = UserSerializer(read_only=True)
    # follows = UserSerializer(read_only=True)
    # follows = SlugRelatedField('username')
    class Meta:
        model = FollowerFollows
        fields = []


class FollowsSerializer(serializers.HyperlinkedModelSerializer):
    follows = UserSerializer(read_only=True)

    class Meta:
        model = FollowerFollows
        fields = ['follows', 'followed']


class FollowedSerializer(serializers.HyperlinkedModelSerializer):
    follower = UserSerializer(read_only=True)

    class Meta:
        model = FollowerFollows
        fields = ['follower', 'followed']
