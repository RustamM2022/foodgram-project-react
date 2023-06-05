from django.contrib import admin

from recipes.models import (Favorites, Ingredient, RecipeIngredient, Recipes,
                            ShoppingList, Tag)


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_display_links = ('name', )
    list_filter = ('name', 'author', 'tag')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_display_links = ('name', )
    list_filter = ('name', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    list_display_links = ('ingredient', )


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('favorite_recipe', 'user')
    list_display_links = ('favorite_recipe', )


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('recipe', )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
