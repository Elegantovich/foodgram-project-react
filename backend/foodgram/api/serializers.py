from recipe.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        model = User


class AuthSerializer(UserSerializer):

    class Meta:
        fields = ('password', 'email')
        model = User


class UserRoleSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')
        model = User

class TokenSerializer(UserSerializer):

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')
