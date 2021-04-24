from django.contrib import admin
from tutorial.quickstart.models import Dag, Tweet, FollowerFollows

# Register your models here.
admin.site.register(Dag)
admin.site.register(Tweet)
admin.site.register(FollowerFollows)
