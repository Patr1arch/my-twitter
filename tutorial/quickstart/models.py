from django.db import models


class Dag(models.Model):
    name = models.CharField(max_length=12)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Tweet(models.Model):
    text = models.CharField(max_length=280)
    photo = models.URLField(blank=True, max_length=512)
    # created = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'[{self.author.username}] {self.text}'


class FollowerFollows(models.Model):
    follower = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='follows')
    follows = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='followers')

    followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} -> {self.follows.username}'
        # return f'{self.follower.username}'
