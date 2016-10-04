from django.db import models


class Test_table(models.Model):
    test = models.CharField(max_length=50)

# Create your models here.
