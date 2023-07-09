from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=250)
    attributes = models.CharField(max_length=250)
    description = models.TextField()
    img = models.CharField(max_length=250)
    world_id = models.ForeignKey("World", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + " " + self.name
