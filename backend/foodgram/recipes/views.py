from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from recipes.mixins import CreateListDestroyViewSet
from recipes.pagination import CustomPagination
from users.permissions import IsAuthorOrReadOnly

from .filters import IngredientFilter, RecipesFilter
from .models import Favorites, Ingredient, Recipes, ShoppingList, Tag
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeEditSerializer, RecipeReadSerializer,
                          ShoppingListSerializer, TagSerializer)

User = get_user_model()


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    pagination_class = CustomPagination
    filterset_class = RecipesFilter
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeEditSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=('get',), detail=False, url_path='download_shopping_cart')
    def download_cart(self, request):
        user = request.user
        if not user.buyer.exists():
            return Response('Список покупок отсутствует',
                            status=status.HTTP_400_BAD_REQUEST)
        filename = 'shopping_list.txt'
        shopping_list = [f'Список покупок пользователя: {user.username}']
        ingredients = Ingredient.objects.filter(
            ingredient__recipe__shopping_recipes__user=user
        ).values('name', 'measurement_unit').annotate(
            amount=Sum('ingredient__amount'))
        for _ in ingredients:
            shopping_list.append(
                f'{_["name"]}: {_["amount"]} {_["measurement_unit"]}')
        shopping_list = '\n'.join(shopping_list)
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FavoriteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    queryset = Recipes.objects.all()
    serializer_class = FavoriteSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)

    def get_recipes(self):
        return get_object_or_404(Recipes, id=self.kwargs.get('recipes_id'))

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user,
                        favorite_recipe=self.get_recipes())

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipes_id):
        try:
            Favorites.objects.get(user=request.user,
                                  favorite_recipe_id=recipes_id).delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT)
        except Favorites.DoesNotExist:
            return Response(
                {'message': 'Рецепта нет в избранном'},
                status=status.HTTP_400_BAD_REQUEST)


class ShoppingListViewSet(CreateListDestroyViewSet):
    serializer_class = ShoppingListSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user,
                        recipe=get_object_or_404(
                            Recipes, id=self.kwargs.get('recipes_id')))

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipes_id):
        try:
            ShoppingList.objects.get(
                user=request.user, recipe=get_object_or_404(
                    Recipes, id=self.kwargs.get('recipes_id'))).delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT)
        except ShoppingList.DoesNotExist:
            return Response(
                {'message': 'Рецепта нет в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST)
