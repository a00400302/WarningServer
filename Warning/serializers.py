from rest_framework import serializers
from Warning.models import PushUser, WarningHistory
from django.contrib.auth.models import User


class PushSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushUser
        fields = '__all__'


class WaringSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarningHistory
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']


