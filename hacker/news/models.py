from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Story(models.Model):
    story_id = models.IntegerField()
    username = models.CharField(max_length=32)
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=64, null=True)
    score = models.CharField(max_length=32)
    description = models.TextField(null=True)
    sentiment = models.CharField(max_length=32)
    rank = models.IntegerField()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
