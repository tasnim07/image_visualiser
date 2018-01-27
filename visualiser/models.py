from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Image(models.Model):
    url = models.URLField(max_length=300)
    last_modified = models.DateTimeField(auto_now_add=True)

    def get_labels(self):
        return self.label_annotation.all()

    def get_text(self):
        return self.text_annotation.all()

    def __str__(self):
        return self.url


class LabelAnnotation(models.Model):
    mid = models.CharField(max_length=30)
    description = models.TextField()
    score = models.FloatField()
    topicality = models.FloatField()
    image = models.ForeignKey(Image, related_name='label_annotation',
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TextAnnotation(models.Model):
    text = models.TextField()
    # locale = models.CharField(max_length=10, blank=True, null=True)
    image = models.ForeignKey(Image, related_name='text_annotation',
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.description
