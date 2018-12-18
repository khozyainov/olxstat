from django.db import models

# Create your models here.
class Submarket(models.Model):
    email = models.EmailField(blank=False, null=False)
    submarketurl = models.URLField(blank=False, null=False)


class Post(models.Model):
    submarket = models.ForeignKey('Submarket', on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
