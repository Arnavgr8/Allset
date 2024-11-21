from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=130)
    phone = models.CharField(max_length=13)
    message = models.TextField()


    def __str__(self):
        return f"{self.name}'s message"
