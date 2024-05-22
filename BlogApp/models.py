from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    is_published = models.BooleanField(default=False, null=True, blank=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    category = models.TextField(blank=False, null=True)

    def __str__(self):
        return self.title
