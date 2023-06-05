from django.contrib import admin

from recipes.models import Subscription

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email',
                    'is_subscribed')
    list_display_links = ('username', )
    list_editable = ('is_subscribed',)
    list_filter = ('username', 'email')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', 'created')
    list_display_links = ('author', )


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
