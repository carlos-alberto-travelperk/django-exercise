from rest_framework import viewsets

from recipe.models import Ingredient, Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return self.queryset.order_by("-id")


class IngredienteViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        return self.queryset.order_by("-name")
