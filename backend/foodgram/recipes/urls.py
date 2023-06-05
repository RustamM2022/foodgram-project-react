from django.urls import include, path
from rest_framework import routers

from .views import (FavoriteViewSet, IngredientViewSet, RecipesViewSet,
                    ShoppingListViewSet, TagViewSet)

app_name = 'recipes'

router = routers.DefaultRouter()

router.register(r'recipes', RecipesViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(
    r'^recipes/(?P<recipes_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorites')
router.register(
    r'^recipes/(?P<recipes_id>\d+)/shopping_cart',
    ShoppingListViewSet,
    basename='shopping_cart')

urlpatterns = [
    path('', include(router.urls))
]
