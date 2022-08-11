from rest_framework import viewsets

from recipe.models import Ingredient, Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        queryset = self.queryset.order_by("-id")
        filter_by_name = self.request.GET.get('name', None)
        if filter_by_name is not None:
            queryset = queryset.filter(name__contains=filter_by_name)

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        for ingredient in instance.ingredients.all():
                ing = Ingredient.objects.filter(id=ingredient.id)
                ing.delete()

        return super().destroy(request, *args, **kwargs)

class IngredienteViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        return self.queryset.order_by("-name")
