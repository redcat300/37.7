from django.db import models
from django.conf import settings
from users.models import CustomUser

CATEGORY_CHOICES = [
    ('TANKS', 'Танки'),
    ('HEALERS', 'Хилы'),
    ('DPS', 'ДД'),
    ('TRADERS', 'Торговцы'),
    ('GUILDMASTERS', 'Гилдмастеры'),
    ('QUESTGIVERS', 'Квестгиверы'),
    ('BLACKSMITHS', 'Кузнецы'),
    ('LEATHERWORKERS', 'Кожевники'),
    ('POTIONMAKERS', 'Зельевары'),
    ('SPELLMASTERS', 'Мастера заклинаний'),
]

class Ad(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='ads/images/', null=True, blank=True)
    video = models.FileField(upload_to='ads/videos/', null=True, blank=True)

    def __str__(self):
        return self.title

class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Response by {self.author} on {self.ad}'



class Comment(models.Model):
    ad = models.ForeignKey(Ad, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    video = models.FileField(upload_to='comment_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.ad}'


class Like(models.Model):
    ad = models.ForeignKey(Ad, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
