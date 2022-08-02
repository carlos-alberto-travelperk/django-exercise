from django.test import TestCase

from recipe import models

class ModelTests(TestCase):

    def test_create_recipe(self):
        recipe = models.Recipe.objects.create(
            name="pizza",
            description="desc_sample"
        )

        self.assertEqual("Name: pizza. Description: desc_sample", str(recipe))

    def test_create_ingredient(self):
        ingredient = models.Ingredient.objects.create(
            name="Tomate"
        )

        self.assertEqual("Name: Tomate", str(ingredient))
