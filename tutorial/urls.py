"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.contrib import admin
from django.urls import include, path
from rest_framework_extensions.routers import ExtendedDefaultRouter
from tutorial.quickstart import views
from tutorial.quickstart.router import SwitchDetailRouter

router = ExtendedDefaultRouter()
switch_router = SwitchDetailRouter()

user_router = router.register(r'users', views.UserViewSet)
user_router.register(
    r'tweets', views.UserTweetsViewSet, 'user-tweets', ['username'])
user_router.register(r'follows', views.FollowsListViewSet, 'user-follows', ['username'])
user_router.register(r'followed', views.FollowedListViewSet, 'user-followed', ['username'])
router.register(r'dags', views.DagViewSet)
router.register(r'tweets', views.TweetViewSet)
switch_router.register(r'follow', views.FollowViewSet)
router.register(r'feed', views.FeedViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(switch_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls)
]
