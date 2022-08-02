from pyexpat import model
from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return "Name: " + self.name + \
            ". Description: " + self.description


class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "Name: " + self.name