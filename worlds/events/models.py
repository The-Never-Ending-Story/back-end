from django.db import models

class Event(models.Model):
    description = models.TextField()
    world_id = models.ForeignKey("World", on_delete=models.CASCADE)
    location_id = models.ForeignKey("Location", on_delete=models.CASCADE)
    time = models.TextField(default='none')


    def __str__(self):
        return str(self.id)