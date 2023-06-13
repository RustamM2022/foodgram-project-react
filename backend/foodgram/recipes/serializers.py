from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import User
from users.serializers import UserSerializer

from .models import (Favorites, Ingredient, RecipeIngredient, Recipes,
                     ShoppingList, Subscription, Tag)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientEditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class IngredientRecipesSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientRecipesSerializer(
        many=True, required=True, source='recipe')
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and ShoppingList.objects.filter(
            user=user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and Favorites.objects.filter(
            user=user, favorite_recipe=obj).exists()

    class Meta:
        model = Recipes
        fields = (
            'id', 'author', 'ingredients', 'tags',
            'text', 'is_in_shopping_cart',
            'is_favorited', 'name', 'cooking_time', 'image')


class RecipeEditSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    ingredients = IngredientEditSerializer(many=True)
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipes
        fields = "__all__"

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.bulk_create([
                RecipeIngredient(recipe=recipe,
                                 ingredient_id=ingredient.get('id'),
                                 amount=ingredient.get('amount'))])

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if 'tags' in validated_data:
            instance.tags.set(validated_data.pop('tags'))
        return super().update(instance, validated_data)

    def validate(self, data):
        ingredients = data.get('ingredients')
        if len(ingredients) != len(set(
                [ingredient['id'] for ingredient in ingredients])):
            raise serializers.ValidationError(
                'Ингредиент не должен повторяться'
            )
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='recipes.id',
    )
    name = serializers.ReadOnlyField(
        source='recipes.name',
    )
    image = serializers.CharField(
        source='recipes.image',
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source='recipes.cooking_time',
    )

    def validate(self, data):
        user = self.context.get('request').user
        favorite_recipe_id = self.context.get('view').kwargs.get('recipes_id')
        if Favorites.objects.filter(
            user=user,
                favorite_recipe=favorite_recipe_id).exists():
            raise serializers.ValidationError(
                'Рецепт уже в избранном'
            )
        return data

    class Meta:
        model = Favorites
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context.get('request').user, author=obj).exists()

    def get_recipes(self, obj):
        recipes = Recipes.objects.filter(author=obj)
        return SubscriptionRecipeSerializer(
            recipes, many=True).data

    def get_recipes_count(self, obj):
        return Subscription.objects.filter(author=obj).count()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'user',
            'author'
        )

    def validate(self, data,):
        user = self.context.get('request').user
        author = self.instance
        if Subscription.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на данного автора'
            )
        if user == author:
            raise serializers.ValidationError(
                'Подписка на самого себя запрещена!')
        return data


class SubscriptionReadSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context.get('request').user, author=obj).exists()

    def get_recipes(self, obj):
        recipes = Recipes.objects.filter(author=obj)
        return SubscriptionRecipeSerializer(
            recipes, many=True).data

    def get_recipes_count(self, obj):
        return Subscription.objects.filter(author=obj).count()


class ShoppingListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    image = serializers.ImageField(read_only=True)
    name = serializers.ReadOnlyField(source='recipe.name')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingList
        fields = (
            'id', 'name', 'cooking_time', 'image')
