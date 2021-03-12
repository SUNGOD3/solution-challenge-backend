from rest_framework import serializers

from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'nickname', 'role', 'bio', 'career', 'verify', 'verify_code')
