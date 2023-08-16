from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=2000)
    thumbnail_url = models.URLField(blank=True, default="https://i.ibb.co/3RLm4Jc/629a49e7ab53625cb2c4e791-Brand-pattern.jpg")
    title = models.CharField(max_length=512, blank=True)
    description = models.TextField(blank=True)
    note = models.TextField(blank=True)
    tags = models.ManyToManyField("Tag", blank=True)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey("Collection", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
      return self.name