import json
from django.db import models


# Create your models here.
class WordList(models.Model):
    words_raw = models.TextField()
    words_clean = models.JSONField()

    def save(self, *args, **kwargs):
        self.words_clean = self.words_raw.split('\r\n')
        super().save(*args, **kwargs)


class Pattern(models.Model):
    words = models.ForeignKey(WordList, null=True, on_delete=models.CASCADE)
    locations = models.JSONField()
    dimensions = models.JSONField(null=True)
    cross = models.JSONField(null=True)
    down = models.JSONField(null=True)
    ordering = models.JSONField(null=True)

    def unpack(self):
        fields = ['locations', 'dimensions', 'cross', 'down', 'ordering']
        return {f:getattr(self, f) for f in fields}
