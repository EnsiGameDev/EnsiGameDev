from django.db import models

# Create your models here.
class Game(models.Model):
    picture = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100)
    index = models.CharField(max_length=100)

    def __str__(self):
        return self.name