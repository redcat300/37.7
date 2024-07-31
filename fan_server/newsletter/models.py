from django.db import models
from django.conf import settings
from ads.models import CATEGORY_CHOICES

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subscribed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.category}"
