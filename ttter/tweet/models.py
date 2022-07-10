from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
import uuid
User = get_user_model()


class Tweet(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(verbose_name='content', max_length=200)
    created_at = models.DateTimeField(
        verbose_name='create_date', default=timezone.now)
