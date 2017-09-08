from rest_framework import serializers
from . import models

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = '__all__'

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contributor
        fields = '__all__'

class CountryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CountryTag
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'

class TagGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TagGroup
        fields = '__all__'
