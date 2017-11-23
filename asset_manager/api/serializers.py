from rest_framework import serializers
from file_manager import models

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        fields = ('id', 'name', 'file', 'link', 'description', 'duration', \
            'creation_date', 'copyright_info', 'enabled', 'status', \
            'type_field', 'filetype', 'uploaded_at', 'last_edit_at', \
            'tags', 'locations', 'contributors', 'collections', )

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ('id', 'name', )

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contributor
        fields = ('id', 'name', )

class CountryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CountryTag
        fields = ('id', 'name', 'code', )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'group', )

class TagGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TagGroup
        fields = ('id', 'name', )
