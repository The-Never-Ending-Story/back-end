from django.db import models

class World(models.Model):
    username = models.CharField(max_length=250)