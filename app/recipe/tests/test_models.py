from django.test import TestCase

from recipe import models

class ModelTests(TestCase):

    def test_create_recipe(self):
        recipe = models.Recipe.objects.create(
            name="pizza",
            description="desc_sample",
        )

        self.assertEqual(recipe.name, "pizza")
        self.assertEqual(recipe.description, "desc_sample")

    def test_create_ingredient(self):
        ingredient = models.Ingredient.objects.create(
            name="Tomate"
        )

        self.assertEqual("Name: Tomate", str(ingredient))
