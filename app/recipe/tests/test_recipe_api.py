from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from urllib.parse import urlencode

from recipe.models import Recipe, Ingredient

from recipe.serializers import RecipeSerializer


def get_recipies_url(recipe_id=None):
    if recipe_id:
        return reverse('recipe:recipe-detail', args=[recipe_id])
    return reverse('recipe:recipe-list')


def url_with_querystring(**kwargs):
    return get_recipies_url() + '?' + urlencode(kwargs)


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

        res = self.client.get(get_recipies_url())

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe_with_an_ingredient(self):
        payload = {
            "name": "Sample recipe name",
            "description": "Sample description",
            "ingredients": [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]
        }

        res = self.client.post(get_recipies_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.all().order_by("-id")
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 3)

    def test_update_recipe_with_new_ingredient(self):
        ingredient1 = Ingredient.objects.create(name='Pepper')
        recipe = create_recipe()
        recipe.ingredients.add(ingredient1)

        ingredient2 = Ingredient.objects.create(name='Chili')
        payload = {'ingredients': [{'name': 'Chili'}]}
        url = get_recipies_url(recipe.id)

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(ingredient2, recipe.ingredients.all())
        self.assertNotIn(ingredient1, recipe.ingredients.all())

    def test_the_ingredients_are_deleted_when_recipe_is_deleted(self):
        ingredient = Ingredient.objects.create(name='Pepper')
        recipe = create_recipe()
        recipe.ingredients.add(ingredient)

        all_ingredients = Ingredient.objects.all()
        self.assertEqual(all_ingredients.count(), 1)

        url = get_recipies_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        deleted_ingredient = Ingredient.objects.filter(id=ingredient.id)
        self.assertFalse(deleted_ingredient.exists())

    def test_filter_by_recipe_name(self):
        create_recipe(name="Pizza")
        create_recipe(name="Curry")

        url = url_with_querystring(name='Pi')

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        expected_recipe = Recipe.objects.filter(name="Pizza").order_by("-id")
        expected = RecipeSerializer(expected_recipe, many=True)
        self.assertEqual(expected.data, res.data)
