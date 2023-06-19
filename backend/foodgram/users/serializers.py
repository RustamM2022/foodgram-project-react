import re

from djoser.serializers import (PasswordSerializer, UserCreateSerializer,
                                UserSerializer)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Subscription
from users.models import User


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(
                user=user, author=obj).exists()

    class Meta:
        fields = (
            'id', 'username', 'email', 'first_name',
            'last_name', 'is_subscribed')
        model = User


class UserCreateSerializer(UserCreateSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'password')
        model = User
        required_fields = (
            'username', 'email', 'first_name', 'last_name', 'password')
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username', 'email')
        )
        ]

    def validate(self, data):
        if not re.match(r'^[\w.@+-]+', str(data.get('username'))):
            raise serializers.ValidationError(
                "Неверный формат имени."
            )
        return data


class SetPasswordSerializer(PasswordSerializer):
    current_password = serializers.CharField(required=True)

    class Meta:
        fields = (
            'current_password', 'new_password')

    def validate(self, data):
        if data['current_password'] == data['new_password']:
            raise serializers.ValidationError(
                'Пароль не изменился'
            )
        return data
