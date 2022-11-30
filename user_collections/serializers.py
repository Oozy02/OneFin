from rest_framework import serializers
from .models import Collections, Movies


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = ['user_id', 'title', 'description', 'collection_uuid']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['title', 'description', 'movie_uuid', 'genre', 'collection_uuid']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
