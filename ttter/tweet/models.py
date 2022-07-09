from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

class Tweet(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(verbose_name='content', max_length=200)
    created_at = models.DateTimeField(verbose_name='create_date', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='update_date', blank=True, null=True)