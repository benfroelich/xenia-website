from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
    bio = models.TextField(max_length=250)

class Social(models.Model):
    url = models.URLField()
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
