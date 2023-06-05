from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from .models import Ingredient, Recipes, Tag

User = get_user_model()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipesFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(
        field_name='author', queryset=User.objects.all())
    tag = filters.ModelMultipleChoiceFilter(to_field_name='slug',
                                            field_name='tag__slug',
                                            queryset=Tag.objects.all())
    is_favorited = filters.BooleanFilter(method='get_is_favorited')

    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(recipes__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_recipes__user=user)
        return queryset

    class Meta:
        model = Recipes
        fields = ('author', 'tag', 'is_favorited', 'is_in_shopping_cart')
