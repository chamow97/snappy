from django.db import models

from twitter_snaps.forms import UserForm


class user_search(models.Model):
    search_term = models.CharField(max_length=100)
    time = models.DateTimeField()
    platform = models.IntegerField()
    user_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.search_term + "  " + self.user_name