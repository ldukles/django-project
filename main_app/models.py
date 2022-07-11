from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    classification = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.classification}'

    def get_absolute_url(self):
        return reverse('categorys_detail', kwargs={'pk': self.id})


class Observation(models.Model):
    name = models.CharField(max_length=100)
    sciname = models.CharField(max_length=100)
    amount = models.IntegerField()
    date = models.DateField('')
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    details = models.CharField(max_length=250)
    categorys = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'observation_id': self.id})