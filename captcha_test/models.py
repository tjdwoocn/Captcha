from django.db import models


class TextCaptcha(models.Model):
    answer = models.CharField(max_length=50)
    response = models.CharField(max_length=100)
    create_date = models.DateTimeField('date published')

    def __str__(self):
        return self.answer


class ImageCaptcha(models.Model):
    topic = models.CharField(max_length=50)
    checked_lists = models.CharField(max_length=500)
    create_date = models.DateTimeField('date published')

    def __str__(self):
        return self.topic
