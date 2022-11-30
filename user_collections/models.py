from django.db import models
import uuid
from users.models import User

# Create your models here.


class Collections(models.Model):
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    collection_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=1000)
   
    
class Movies(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=1000)
    movie_uuid = models.CharField(primary_key= True, max_length=255, blank=False)
    genre = models.CharField(max_length=255, blank=False)
    collection_uuid = models.ForeignKey(Collections, null=True, on_delete=models.CASCADE)
   
