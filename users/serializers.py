from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data['password']
        if password is not None:
            validated_data['password'] = make_password(password)
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
