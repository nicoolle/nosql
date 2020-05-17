from djongo import models


class Comment(models.Model):
    author = models.CharField(blank=False, max_length=40)
    content = models.TextField(blank=False)


class Post(models.Model):
    author = models.CharField(blank=False, max_length=40)
    title = models.CharField(blank=False, max_length=100)
    content = models.TextField(blank=False)
    comments = models.ArrayField(Comment)

