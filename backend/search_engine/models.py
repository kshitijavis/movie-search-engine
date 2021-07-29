from django.db import models

class Movie(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    tagline = models.CharField(max_length=500, default='')
    overview = models.CharField(max_length=2000, default='')
    vote_average = models.DecimalField(max_digits=3, decimal_places=1, default=0)

    keywords = models.ManyToManyField('Keyword', related_name='movies')

    def __str__(self):
        return self.title

class Keyword(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name