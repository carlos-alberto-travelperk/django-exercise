from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse("recipe:recipe-list")


def create_recipe(**params):
    defaults = {
        "name": "Sample recipe name",
        "description": "Sample description",
    }
    defaults.update(params)

    recipe = Recipe.objects.create(**defaults)
    return recipe


class RecipeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrive_recipes(self):
        create_recipe()
        create_recipe()

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
