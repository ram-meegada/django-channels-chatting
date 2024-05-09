from django.db import models

# Create your models here.
class ElasticSearchModel(models.Model):
    title = models.TextField()
    content = models.TextField()