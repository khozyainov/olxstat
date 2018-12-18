from django.db import models

# Create your models here.
from django.urls import reverse


class Submarket(models.Model):
    email = models.EmailField(blank=False, null=False)
    submarketurl = models.URLField(blank=False, null=False)

    def get_absolute_url(self):
        return reverse('submarket', args=[str(self.id)])


class Post(models.Model):
    submarket = models.ForeignKey('Submarket', on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
