from django.db import models
from api.models import User

class UserFollowersFollowingModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    following = models.ManyToManyField(User, blank=True, related_name="following")
    def __str__(self):
        return self.user.email