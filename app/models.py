from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, null=False)
    # user = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=255, null=False)
    body = models.TextField()
    profile = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)


class Comment(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, null=False)
    body = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

