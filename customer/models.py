from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=127)
    born = models.DateField()
    CPF = models.CharField(max_length=14, unique=True, db_index=True)

    def __str__(self):
        return self.name
